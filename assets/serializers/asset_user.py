from rest_framework import serializers
from ..models.asset import AssetUser, Asset
from ..utils import get_object_or_none


class AssetUserSerializer(serializers.ModelSerializer):
    # 设置日期格式化格式
    updated_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', required=False)

    class Meta:
        model = AssetUser
        # fields = ['id', 'is_admin', 'username', 'password', 'updated_time']
        fields = '__all__'
