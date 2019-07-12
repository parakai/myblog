from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

app_name = 'assets'

router = DefaultRouter()
router.register('nodes', views.NodeViewSet, 'node')
router.register('assets', views.AssetViewSet, 'asset')

urlpatterns = [
    path('', include(router.urls)),
    path('tree/', views.treeview, name="tree"),
    path('treenode/', views.NodeAsTreeApi.as_view(), name='node-tree'),
    path('<uuid:pk>/children/', views.NodeChildrenApi.as_view(), name='node-children'),
    path('<uuid:pk>/children/add/', views.NodeAddChildrenApi.as_view(), name='node-add-children'),
    path('asset/create/', views.AssetCreateView.as_view(), name='assets-create'),
    path('asset/list/', views.AssetListView.as_view(), name='assets-list'),
]
