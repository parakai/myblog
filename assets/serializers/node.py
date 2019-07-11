from rest_framework import serializers
from assets.models.node import Node


class NodeSerializer(serializers.ModelSerializer):
    assets_amount = serializers.IntegerField(read_only=True)

    class Meta:
        model = Node
        fields = [
            'id', 'key', 'value', 'child_mark', 'assets_amount'
        ]


class NodeAddChildrenSerializer(serializers.Serializer):
    nodes = serializers.ListField()
