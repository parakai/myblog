from django.contrib import admin
from .models import asset


@admin.register(asset.Asset)
class AssetAdmin(admin.ModelAdmin):
    '''资产信息'''
    list_display = ['appinfo', 'hostname', 'ip', 'platform',  'port', 'assettype', 'is_formal', 'model',
                    'cpu_model', 'cpu_count', 'memory', 'disk_total', 'created_by']


@admin.register(asset.AssetUser)
class AssetUserAdmin(admin.ModelAdmin):
    '''用户信息'''
    list_display = ['username', 'password', 'is_admin', 'updated_time']


@admin.register(asset.AppUser)
class AppUserAdmin(admin.ModelAdmin):
    '''用户信息'''
    list_display = ['username', 'password', 'app', 'is_admin', 'updated_time']


@admin.register(asset.AppInfo)
class AppinfoAdmin(admin.ModelAdmin):
    '''应用系统'''
    list_display = ['app_name', 'url', 'created_time']


@admin.register(asset.OperatingSystem)
class OSAdmin(admin.ModelAdmin):
    '''操作系统'''
    list_display = ['name', 'created_time']
