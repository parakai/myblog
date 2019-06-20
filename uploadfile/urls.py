from django.urls import path
from .views import uploadView, upload_file, FileFieldView, DeleteSelectView

urlpatterns = [
    # path('uploads', upload_file, name="uploads"),
    # path('uploads', uploadView.as_view(), name="uploads"),
    path('uploads', FileFieldView.as_view(), name="uploads"),
    path('delfiles/', DeleteSelectView.as_view(), name="delfiles"),
]
