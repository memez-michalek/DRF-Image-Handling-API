from rest_framework import serializers
from .models import User,Img,Plan, Link
from collections import OrderedDict
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
class UploadImageSerializer(serializers.ModelSerializer):
    def to_representation(self, instance):
        result = super(UploadImageSerializer, self).to_representation(instance)
        return OrderedDict([(key, result[key]) for key in result if result[key] is not None])
    class Meta:   
        model = Img
        fields = ['image', 'smaller_thumbnail', 'bigger_thumbnail', 'owner', ]

class SmallThumbnailSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Img
        fields = ["smaller_thumbnail"]
class SmallAndBigThumbailSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Img
        fields = ["smaller_thumbnail", "bigger_thumbnail"]
class SmallThumbnailandOriginalLinkSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Img
        fields = ["smaller_thumbnail", "image"]

class AllFieldsImageSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Img
        fields = ["image", "smaller_thumbnail", "bigger_thumbnail"]

class LinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Link
        fields = "__all__"