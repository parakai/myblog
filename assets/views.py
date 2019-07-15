from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.views.generic.detail import DetailView
from django.views.generic import TemplateView
from django.contrib.messages.views import SuccessMessageMixin
from rest_framework import generics, mixins, viewsets
from rest_framework.serializers import ValidationError
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination

from .tree import TreeNodeSerializer
from assets.models.node import Node
from assets.models.asset import Asset
from .serializers import node, asset
from .utils import get_object_or_none, create_success_msg
from . import forms


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
            queryset = list(self.node.get_all_children(with_self=True))
            nodes_invalid = Node.objects.exclude(key__startswith=self.node.key)
            queryset.extend(nodes_invalid)
        queryset = [node.as_tree_node() for node in queryset]
        return queryset


class NodeChildrenApi(mixins.ListModelMixin, generics.CreateAPIView):
    queryset = Node.objects.all()
    serializer_class = node.NodeSerializer
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


class NodeAddChildrenApi(generics.UpdateAPIView):
    queryset = Node.objects.all()
    serializer_class = node.NodeAddChildrenSerializer
    instance = None

    def put(self, request, *args, **kwargs):
        instance = self.get_object()
        nodes_id = request.data.get("nodes")
        children = [get_object_or_none(Node, id=pk) for pk in nodes_id]
        for node in children:
            if not node:
                continue
            node.parent = instance
        return Response("OK")


class NodeViewSet(viewsets.ModelViewSet):
    queryset = Node.objects.all()
    serializer_class = node.NodeSerializer

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        parent = instance.parent
        parent.child_mark -= 1
        parent.save()
        return super().destroy(self, request, *args, **kwargs)


class AssetViewSet(viewsets.ModelViewSet):
    queryset = Asset.objects.all()
    serializer_class = asset.AssetSerializer
    # pagination_class = AssetPagination
    pagination_class = LimitOffsetPagination
    # filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)

    filter_fields = ('assettype',)
    # 搜索,=name表示精确搜索，也可以使用各种正则表达式
    search_fields = ('name', 'ip', 'model')

    ordering_fields = ('name', 'ip', 'model',)

    def filter_node(self, queryset):
        node_id = self.request.query_params.get("node_id")
        if not node_id:
            return queryset
        node = get_object_or_404(Node, id=node_id)
        if node.is_root():
            return queryset
        else:
            queryset = queryset.filter(nodes__key__regex='^{}(:[0-9]+)*$'.format(node.key),)
        return queryset

    def filter_queryset(self, queryset):
        queryset = super().filter_queryset(queryset)
        queryset = self.filter_node(queryset)
        return queryset

    def get_queryset(self):
        queryset = super().get_queryset().distinct()
        return queryset


class AssetCreateView(SuccessMessageMixin, CreateView):
    model = Asset
    template_name = 'node/asset_create.html'
    form_class = forms.AssetCreateForm
    success_url = reverse_lazy('assets:assets-list')

    def get_form(self, form_class=None):
        form = super().get_form(form_class=form_class)
        node_id = self.request.GET.get("node_id")
        if node_id:
            node = get_object_or_none(Node, id=node_id)
        else:
            node = Node.root()
        form["nodes"].initial = node
        return form

    def get_success_message(self, cleaned_data):
        return create_success_msg % ({"name": cleaned_data["name"]})


class AssetListView(TemplateView):
    template_name = 'node/tree.html'


class AssetDetailView(DetailView):
    model = Asset
    context_object_name = 'asset'
    template_name = 'node/asset_detail.html'
