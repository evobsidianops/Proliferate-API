from django.contrib import admin
from .models import CustomUser, UserInfo

admin.site.register(CustomUser)
admin.site.register(UserInfo)
