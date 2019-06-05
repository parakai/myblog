from django.contrib import admin
from .models import Category, Tag, Blog


class BlogAdmin(admin.ModelAdmin):
    list_display = ['title', 'created_time', 'updated_time', 'category', 'author']


admin.site.register(Category)
admin.site.register(Tag)
admin.site.register(Blog, BlogAdmin)
