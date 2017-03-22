from django.contrib import admin

# Register your models here.
from .models import *

class ShareZoneModel(admin.ModelAdmin):
    list_display = [
        'pk',
        'zipCode',
        'has_CommunityShed',
        'CommunityShedLocation',
    ]

    class Meta:
        model = ShareZone

        
admin.site.register(ToolsRegister)
admin.site.register(UserProfile)
admin.site.register(ShareZone, ShareZoneModel)

