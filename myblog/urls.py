from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name="index"),
    path('ckeditor', include('ckeditor_uploader.urls')),
    path('blog/', include('blog.urls')),
    path('comment/', include('comment.urls')),
    path('soft/', include('uploadfile.urls')),
    path('assets/', include('assets.urls', namespace='assets')),
    path('login/', views.login, name="login"),
    path('login_modal/', views.loginModal, name="login_modal"),
    path('register/', views.register, name="register"),
    path('logout/', views.logout, name="logout"),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
