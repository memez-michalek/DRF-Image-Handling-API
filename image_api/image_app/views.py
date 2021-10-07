from django.shortcuts import render
from rest_framework import generics
from rest_framework import status
from rest_framework.mixins import  CreateModelMixin, RetrieveModelMixin
from rest_framework import viewsets
from .serializers import (UploadImageSerializer,
                          SmallThumbnailSerializer,
                          SmallAndBigThumbailSerializer,
                          SmallThumbnailandOriginalLinkSerializer,
                          AllFieldsImageSerializer,
                          LinkSerializer
                         )
                         
import uuid
import time
import datetime
from .models import Img, User,  Link
from rest_framework.response import Response


class CreateListOverride(generics.GenericAPIView):
    
    def create(self, request, *args, **kwargs):
        owner_id = request.data.get('owner')
        thumbnail = request.data.get('image')
        plan = User.objects.get(id=owner_id).plan
        original_link = plan.is_original_upload_link_avalible
        bigger_thumbnail = plan.is_bigger_thmbnail_avalible
        is_expiring_link = plan.is_expiring_upload_link_avalible

        if is_expiring_link:
            link = uuid.uuid4()
            timeout = request.data.get('link')
            image = Img.objects.create(owner=owner_id, image=thumbnail, expiring_link=timeout)
            image.save()
            l = Link(link_direction=link, img=image, issuedAt=time.time() , timeout=timeout, is_expired=False)
            l.save()
            serializer = UploadImageSerializer(image)
            return Response([serializer.data, l])
        
        else:
            image = Img.objects.create(owner=owner_id, image=thumbnail)
            image.save()
            serializer = UploadImageSerializer(image)
            return Response(serializer.data)
    def list(self, request, pk, *args, **kwargs):
        owner_obj = User.objects.get(pk=pk)
        images = Img.objects.filter(owner=owner_obj)
        original_link = owner_obj.plan.is_original_upload_link_avalible
        bigger_thumbnail = owner_obj.plan.is_bigger_thmbnail_avalible
        serializer = None

        if original_link and bigger_thumbnail:
            serializer =  AllFieldsImageSerializer(images, many=True)
        elif original_link and not bigger_thumbnail:
            serializer = SmallThumbnailandOriginalLinkSerializer(images, many=True)
        elif not original_link and bigger_thumbnail:
            serializer = SmallAndBigThumbailSerializer(images, many=True)
        else:
            serializer = SmallThumbnailSerializer(images, many=True)
    
        return Response(serializer.data)
        
class RetrieveOverride(generics.GenericAPIView):       
    def list(self, request, pk, *args, **kwargs):
        #JWT CHECKIN IF LINK IS VALID
        link_object = Link.objects.get(link_direction=pk)
        issued_at = link_object.issued_at
        
        if int(issued_at.strftime("%H%M%S")) - int(time.time()) > link_object.timeout  or link_object.is_expired:
            return Response(status=status.HTTP_403_FORBIDDEN)

        serializer = UploadImageSerializer(link_object.img)
        return Response(serializer.data)

class PostImageView(CreateModelMixin, CreateListOverride):
    queryset = Img.objects.all()
    serializer_class = UploadImageSerializer
    def post(self, request, *args, **kwargs):
        return self.create(request, *args,  **kwargs)


class ListUserImages(RetrieveModelMixin, CreateListOverride):
    queryset = Img.objects.all()
    def get(self, request,pk, *args, **kwargs):
        return self.list(request,pk, *args, **kwargs)

class RetrieveImageFromLink(RetrieveModelMixin,  RetrieveOverride):
    queryset = Link.objects.all()
    serializer_class = LinkSerializer
    def get(self, request,pk, *args, **kwargs):
        
        return self.list(request,pk, *args, **kwargs)