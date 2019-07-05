from rest_framework import serializers
from assets.models.node import Node


class NodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Node
        fields = [
            'id', 'key', 'value',
        ]


class NodeAddChildrenSerializer(serializers.Serializer):
    nodes = serializers.ListField()
