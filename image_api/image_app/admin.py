from django.contrib import admin
from .models import Plan, Img, User, Link
# Register your models here.

admin.site.register(User)
admin.site.register(Plan)
admin.site.register(Img)
admin.site.register(Link)