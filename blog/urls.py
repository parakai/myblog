from django.urls import path
from . import views


urlpatterns = [
    path('list/', views.blog_list, name="blog_list"),
    path('blog/<int:blog_pk>/', views.blog_detail, name="blog_detail"),
    path('archives/<int:year>/<int:month>', views.archives, name='archives'),
    path('category/<int:category_pk>/', views.category, name='category'),
]
