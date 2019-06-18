from django.contrib import admin
from .models import UploadFile


@admin.register(UploadFile)
class UploadFileAdmin(admin.ModelAdmin):
    list_display = ['title', 'file', 'upload_time']
