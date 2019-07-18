from rest_framework import serializers
from ..models.asset import AssetUser


class AssetUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = AssetUser
        fields = ['id', 'is_admin', 'username', 'password']
