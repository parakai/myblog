from django.db import models
from django.contrib.auth.models import User
from ckeditor_uploader.fields import RichTextUploadingField


class Category(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Blog(models.Model):
    title = models.CharField(max_length=80)
    content = RichTextUploadingField()
    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)
    # 摘要
    # excerpt = models.CharField(max_length=200, blank=True)
    # 记录阅读量
    views = models.PositiveIntegerField(default=0)

    category = models.ForeignKey(Category, on_delete=models.DO_NOTHING)
    tags = models.ManyToManyField(Tag, blank=True)

    author = models.ForeignKey(User, on_delete=models.DO_NOTHING)

    class Meta:
        ordering = ['-created_time']

    def __str__(self):
        return "<Blog: %s>" % self.title
