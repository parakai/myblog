from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views


router = DefaultRouter()
router.register('nodes', views.NodeViewSet, 'node')

urlpatterns = [
    path('', include(router.urls)),
    path('tree/', views.treeview, name="tree"),
    path('treenode/', views.NodeAsTreeApi.as_view(), name='node-tree'),
    path('<uuid:pk>/children/', views.NodeChildrenApi.as_view(), name='node-children'),
    path('<uuid:pk>/children/add/', views.NodeAddChildrenApi.as_view(), name='node-add-children'),
]
