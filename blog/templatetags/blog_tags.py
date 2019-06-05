from django import template

from ..models import Blog, Category

register = template.Library()


@register.simple_tag()
def get_recent_blogs(num=5):
    return Blog.objects.all()[:num]


@register.simple_tag()
def archives():
    return Blog.objects.dates('created_time', 'month', order='DESC')


@register.simple_tag()
def get_categories():
    return Category.objects.all()
