from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from ckeditor_uploader.fields import RichTextUploadingField

from comment.models import Comment


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

    def get_previous_blog(self):
        return self.__class__.objects.filter(created_time__gt=self.created_time).last()

    def get_next_blog(self):
        return self.__class__.objects.filter(created_time__lt=self.created_time).first()

    def get_comments(self):
        blog_content_type = ContentType.objects.get_for_model(self)
        comments = Comment.objects.filter(content_type=blog_content_type, object_id=self.pk)
        return comments

