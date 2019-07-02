from django.shortcuts import render
from django.shortcuts import get_object_or_404
from rest_framework import generics, mixins
from rest_framework.serializers import ValidationError
from rest_framework.response import Response

from .tree import TreeNodeSerializer
from .models import Node
from .serializers import NodeSerializer


def treeview(request):
    return render(request, 'node/tree.html', {})


class NodeAsTreeApi(generics.ListAPIView):
    """
    节点子节点作为树返回，
    [
      {
        "id": "",
        "name": "",
        "pId": "",
        "meta": ""
      }
    ]
    """
    serializer_class = TreeNodeSerializer
    node = None
    is_root = False

    def get_queryset(self):
        node_key = self.request.query_params.get('key')
        if node_key:
            self.node = Node.objects.get(key=node_key)
            queryset = self.node.get_children(with_self=False)
        else:
            self.is_root = True
            self.node = Node.root()
            queryset = list(self.node.get_children(with_self=True))
            nodes_invalid = Node.objects.exclude(key__startswith=self.node.key)
            queryset.extend(nodes_invalid)
        queryset = [node.as_tree_node() for node in queryset]
        return queryset


class NodeChildrenApi(mixins.ListModelMixin, generics.CreateAPIView):
    queryset = Node.objects.all()
    serializer_class = NodeSerializer
    instance = None

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        instance = self.get_object()
        if not request.data.get("value"):
            request.data["value"] = instance.get_next_child_preset_name()
        return super().post(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        instance = self.get_object()
        value = request.data.get("value")
        print(value)
        _id = request.data.get('id') or None
        values = [child.value for child in instance.get_children()]
        if value in values:
            raise ValidationError("相同层级节点名称不能相同！")
        node = instance.create_child(value=value, _id=_id)
        return Response(self.serializer_class(instance=node).data, status=201)

    def get_object(self):
        pk = self.kwargs.get('pk') or self.request.query_params.get('id')
        if not pk:
            node = Node.root()
        else:
            node = get_object_or_404(Node, pk=pk)
        return node
