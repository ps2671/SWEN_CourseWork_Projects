from django.contrib import admin
from .models import *


class UserProfileModel(admin.ModelAdmin):
    list_display = [
        'user',
        'type',
    ]

    class Meta:
        model = UserProfile

admin.site.register(UserProfile, UserProfileModel)


