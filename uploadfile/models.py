from django.db import models


class UploadFile(models.Model):
    title = models.CharField("文件名", max_length=100)
    file = models.FileField("文件路径", upload_to="uploads/%Y/%m")
    upload_time = models.DateTimeField("上传时间", auto_now_add=True)
    # size = models.CharField("文件大小", max_length=20, null=True, blank=True)
    download_nums = models.IntegerField("下载量", default=0)

    def __str__(self):
        return self.title
