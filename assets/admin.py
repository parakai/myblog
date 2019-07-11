from django.contrib import admin
from .models import asset


@admin.register(asset.Asset)
class AssetAdmin(admin.ModelAdmin):
    '''资产信息'''
    list_display = ['appinfo', 'name', 'ip', 'platform',  'port', 'assettype', 'is_formal', 'model',
                    'cpu_model', 'cpu_count', 'memory', 'disk_total', 'created_by']


@admin.register(asset.UserProfileManager)
class UserProfileAdmin(admin.ModelAdmin):
    '''用户信息'''
    list_display = ['asset', 'app', 'is_admin', 'username', 'password', ]


@admin.register(asset.AppInfo)
class AppinfoAdmin(admin.ModelAdmin):
    '''应用系统'''
    list_display = ['app_name', 'url', 'created_time']


@admin.register(asset.OperatingSystem)
class OSAdmin(admin.ModelAdmin):
    '''操作系统'''
    list_display = ['name', 'created_time']
