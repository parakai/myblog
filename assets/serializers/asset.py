from rest_framework import serializers
from ..models import asset


class AppinfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = asset.AppInfo
        fields = ['app_name', 'url']


class OperatingSystemSerializer(serializers.ModelSerializer):
    class Meta:
        model = asset.OperatingSystem
        fields = ['name']


class AssetSerializer(serializers.ModelSerializer):
    os = OperatingSystemSerializer()
    appinfo = AppinfoSerializer()

    class Meta:
        model = asset.Asset
        fields = '__all__'
