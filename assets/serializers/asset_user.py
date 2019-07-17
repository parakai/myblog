from rest_framework import serializers
from ..models.asset import UserProfileManager


class AssetUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfileManager
        fields = ['id', 'is_admin', 'username', 'password', 'asset_id']
