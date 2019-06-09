from django import template
from django.db.models.aggregates import Count

from ..models import Blog, Category

register = template.Library()


@register.simple_tag()
def get_recent_blogs(num=5):
    return Blog.objects.all()[:num]


@register.simple_tag()
def archives():
    return Blog.objects.dates('created_time', 'month', order='DESC')
    # return Blog.objects.extra(select={'created_time': "strftime('%%Y-%%m',created_time)"}).\
    #     values('created_time').annotate(count=Count('created_time')).order_by()


@register.simple_tag()
def get_categories():
    return Category.objects.annotate(num_blogs=Count('blog')).filter(num_blogs__gt=0)
    # return Category.objects.all()
