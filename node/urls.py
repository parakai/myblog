from django.urls import path
from . import views

urlpatterns = [
    path('tree/', views.treeview, name="tree"),
    path('treenode/', views.NodeAsTreeApi.as_view(), name='node-tree'),
    path('<uuid:pk>/children/', views.NodeChildrenApi.as_view(), name='node-children'),
]
