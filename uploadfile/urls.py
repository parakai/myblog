from django.urls import path
from .views import uploadView, upload_file, FileFieldView, DelFileView

urlpatterns = [
    # path('uploads', upload_file, name="uploads"),
    # path('uploads', uploadView.as_view(), name="uploads"),
    path('uploads', FileFieldView.as_view(), name="uploads"),
    path('delfiles', DelFileView.as_view(), name="delfiles")
]
