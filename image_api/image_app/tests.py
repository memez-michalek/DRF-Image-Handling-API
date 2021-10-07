from django.test import TestCase
from rest_framework.test import APITestCase
from django.urls import reverse
from .models import Img
from django.core.files.uploadedfile import SimpleUploadedFile

class ImageTest(APITestCase):
    def test_create_image(self):
        
        with open("test-image.jpeg", 'rb') as image:

            data = {'owner': '1', 'image': image}
            resp = self.client.post("http://localhost:8080/upload", data, format="json")
            self.assertEqual(resp.status_code, 201)
            self.assertEqual(Img.objects.count(), 1)
    def test_get_images(self):
        url = reverse("list_images/user")
        resp = self.client.get("http://localhost:8080/list_images/user/1", format="json")
        self.assertEqual(resp.status_code, 200)