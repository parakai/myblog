from django.urls import path
from .views import uploadView, upload_file, FileFieldView, DelFileView\
from .views import DelFileView2

urlpatterns = [
    # path('uploads', upload_file, name="uploads"),
    # path('uploads', uploadView.as_view(), name="uploads"),
    path('uploads', FileFieldView.as_view(), name="uploads"),
    path('delfiles', DelFileView.as_view(), name="delfiles"),
    path('delfiles2', DelFileView2.as_view(), name="delfiles2")
]
