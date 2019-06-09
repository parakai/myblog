from django.urls import path
from . import views


urlpatterns = [
    path('list/', views.IndexView.as_view(), name="blog_list"),
    path('blog/<int:pk>/', views.BlogDetailView.as_view(), name="blog_detail"),
    path('archives/<int:year>/<int:month>', views.ArchivesView.as_view(), name='archives'),
    path('category/<int:category_pk>/', views.CategoryView.as_view(), name='category'),
]
