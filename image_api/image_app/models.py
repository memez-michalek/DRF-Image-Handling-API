from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
from PIL import Image
import logging
import os

class Plan(models.Model):
    name = models.CharField(max_length=64)
    is_bigger_thmbnail_avalible = models.BooleanField(default=False)
    is_original_upload_link_avalible = models.BooleanField(default=False)
    expiring_link = models.BooleanField(default=False)
    smaller_thumbnail_size = models.IntegerField(default=200)
    bigger_thumbnail_size = models.IntegerField(default=400)
    
class User(models.Model):
    plan = models.OneToOneField(Plan, on_delete=models.CASCADE)

class Img(models.Model): 
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="default/")
    smaller_thumbnail = models.ImageField(editable=False)
    bigger_thumbnail = models.ImageField(editable=False)
    expiring_link = models.URLField(editable=False, null=True, blank=True)

    def save(self, *args, **kwargs):
        original_image = self.image
        temp_link = self.expiring_link
        plan = User.objects.get(pk=self.owner.pk).plan
        
        if not os.path.exists(f"media/{plan.smaller_thumbnail_size}px"):
            os.mkdir(f"media/{plan.smaller_thumbnail_size}px")
        
        img = Image.open(self.image)
        w, _ = img.size
        img.thumbnail((w, plan.smaller_thumbnail_size), Image.ANTIALIAS)
        file_name = self.image.path.split("/")[-1]
        path = f"media/{plan.smaller_thumbnail_size}px/" + file_name
        img.save(path)
        
        self.smaller_thumbnail = f"{plan.smaller_thumbnail_size}px/" + file_name
        self.image = None
        self.expiring_link = None

        if plan.is_bigger_thmbnail_avalible:
            if not os.path.exists(f"media/{plan.bigger_thumbnail_size}px"):
                os.mkdir(f"media/{plan.bigger_thumbnail_size}px")
            
            image = Image.open(original_image)
            w, _ = image.size
            image.thumbnail((w, plan.bigger_thumbnail_size), Image.ANTIALIAS)
            file_name = original_image.path.split("/")[-1]
            path = f"media/{plan.bigger_thumbnail_size}px/" + file_name    
            image.save(path)
            self.bigger_thumbnail = f"{plan.bigger_thumbnail_size}px/" + file_name
        
        if plan.is_original_upload_link_avalible:
            self.image = original_image
        
        if plan.expiring_link:
            self.expiring_link = temp_link
        
        super().save(*args, **kwargs)

class Link(models.Model):
    link_direction =  models.CharField(max_length=128, unique=True)
    img = models.OneToOneField(Img, on_delete=models.CASCADE)
    issued_at= models.TimeField(auto_now_add=True)
    timeout =  models.IntegerField(default=300)
    is_expired = models.BooleanField(default=False)
