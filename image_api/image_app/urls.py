from django.urls import include, path
from .views import PostImageView, ListUserImages, RetrieveImageFromLink
from django.conf.urls.static import static
from django.conf import settings
#from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    
    path("upload/", PostImageView.as_view(), name="upload"),
    path("list_images/user/<int:pk>", ListUserImages.as_view(), name="list_images"),
    path("link/<str:pk>", RetrieveImageFromLink.as_view(), name="link"),
    ] +static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
