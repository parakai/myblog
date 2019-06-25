from django.shortcuts import render
from rest_framework import generics

from .tree import TreeNodeSerializer
from .models import Node


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
