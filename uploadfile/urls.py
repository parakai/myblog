from django.urls import path, re_path
from .views import uploadView, upload_file, FileFieldView, DeleteSelectView, file_download, DownloadView2

urlpatterns = [
    # path('uploads', upload_file, name="uploads"),
    # path('uploads', uploadView.as_view(), name="uploads"),
    path('uploads', FileFieldView.as_view(), name="uploads"),
    path('delfiles/', DeleteSelectView.as_view(), name="delfiles"),
    re_path(r'^download/(?P<file_path>.*)/$', file_download, name='file_download'),
    path('downs/<int:file_pk>/', DownloadView2.as_view(), name="downloads2"),
]
