from rest_framework import serializers


class TreeNode:
    id = ""
    name = ""
    comment = ""
    title = ""
    isParent = False
    pId = ""
    open = False
    iconSkin = ""
    meta = {}

    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)

    def __str__(self):
        return '<{}: {}>'.format(self.id, self.name)


class TreeNodeSerializer(serializers.Serializer):
    id = serializers.CharField(max_length=128)
    name = serializers.CharField(max_length=128)
    title = serializers.CharField(max_length=128)
    pId = serializers.CharField(max_length=128)
    isParent = serializers.BooleanField(default=False)
    open = serializers.BooleanField(default=False)
    iconSkin = serializers.CharField(max_length=128, allow_blank=True)
    meta = serializers.JSONField()