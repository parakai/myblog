from django.shortcuts import render, HttpResponse
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.detail import DetailView
from django.views.generic import TemplateView
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import Q
from rest_framework import generics, mixins, viewsets, status
from rest_framework.serializers import ValidationError
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination

from .tree import TreeNodeSerializer
from assets.models.node import Node
from assets.models.asset import Asset, AssetUser
from .serializers import node, asset, asset_user
from .utils import get_object_or_none, create_success_msg, update_success_msg
from .forms import AssetCreateForm, AssetUpdateForm, AssetUserUpdateForm
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def report(request):
    if request.method == "POST":
        asset_data = request.POST.get('asset_data')
        print(asset_data)
        return HttpResponse("成功收到数据！")


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
    search_fields = ('hostname', 'ip', 'model', 'platform')

    ordering_fields = ('hostname', 'ip', 'model',)

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
    form_class = AssetCreateForm
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

    def get_context_data(self, **kwargs):
        nodes_remain = Node.objects.exclude(
            Q(assets=self.object))
        context = {
            'nodes_remain': nodes_remain,
        }
        kwargs.update(context)
        return super().get_context_data(**kwargs)


class AssetUserListView(DetailView):
    model = Asset
    context_object_name = 'asset'
    template_name = 'node/asset_asset_user_list.html'

    # def get_context_data(self, **kwargs):
    #     assetuser_remain = AssetUser.objects.exclude(assets=self.object)
    #     context = {
    #         'assetuser_remain': assetuser_remain,
    #     }
    #     kwargs.update(context)
    #     return super().get_context_data(**kwargs)


class AssetUpdateView(SuccessMessageMixin, UpdateView):
    model = Asset
    form_class = AssetUpdateForm
    template_name = 'node/asset_update.html'
    success_url = reverse_lazy('assets:assets-list')

    def get_success_message(self, cleaned_data):
        return update_success_msg % ({"name": cleaned_data["hostname"]})


class AssetUserViewSet(viewsets.ModelViewSet):
    pagination_class = LimitOffsetPagination
    queryset = AssetUser.objects.all()
    serializer_class = asset_user.AssetUserSerializer
    # http_method_names = ['get', 'post']

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        # Asset.objects.get(id=asset_id).assetuser.clear()
        assetuser_oldid = request.data.get('pk')
        asset_id = request.data.get('asset')
        assetuser = AssetUser.objects.get(id=assetuser_oldid)
        # 移除assetuser
        Asset.objects.get(id=asset_id).assetuser.remove(assetuser)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        assetuser_newid = serializer.data.get('id')
        assetuser2 = AssetUser.objects.get(id=assetuser_newid)
        # 添加新元素对应关系
        Asset.objects.get(id=asset_id).assetuser.add(assetuser2)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def get_queryset(self):
        asset_id = self.request.query_params.get("asset_id")
        if asset_id:
            queryset = AssetUser.objects.filter(assets=asset_id)
        else:
            queryset = self.queryset
        return queryset


class AssetUserAddView(generics.CreateAPIView):

    def post(self, request, *args, **kwargs):
        assetuserIds = self.request.data.get("assetuserIds")
        pk = self.kwargs.get('pk')
        asset = get_object_or_404(Asset, pk=pk)
        for userid in assetuserIds:
            asset_user = AssetUser.objects.get(id=userid)
            asset.assetuser.add(asset_user)
        return Response("OK", status=status.HTTP_201_CREATED)


class AssetUserListRemainView(generics.ListAPIView):
    serializer_class = asset_user.AssetUserSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def get_queryset(self):
        pk = self.kwargs.get('pk') or self.request.query_params.get('id')
        asset = get_object_or_404(Asset, pk=pk)
        assetuser = AssetUser.objects.exclude(assets=asset)
        return assetuser


class AssetUserDeleteView(generics.DestroyAPIView):

    def delete(self, request, *args, **kwargs):
        assetuserId = self.request.data.get("assetuserId")
        pk = self.kwargs.get('pk')
        asset = get_object_or_404(Asset, pk=pk)
        asset_user = AssetUser.objects.get(id=assetuserId)
        asset.assetuser.remove(asset_user)
        return Response(status=status.HTTP_204_NO_CONTENT)



