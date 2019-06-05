from django.shortcuts import render, get_object_or_404

from .models import Blog, Category


def blog_list(request):
    blog_lists = Blog.objects.all()
    return render(request, 'blog/list.html', context={
        'blog_lists': blog_lists,
    })


def blog_detail(request, blog_pk):
    blog = get_object_or_404(Blog, pk=blog_pk)
    if not request.COOKIES.get('blog_%s_readed' % blog_pk):
        blog.views += 1
        blog.save()
    previous_blog = Blog.objects.filter(created_time__gt=blog.created_time).last()
    next_blog = Blog.objects.filter(created_time__lt=blog.created_time).first()
    response = render(request, 'blog/detail.html', context={'blog': blog,
                      'previous_blog': previous_blog, 'next_blog': next_blog})
    response.set_cookie('blog_%s_readed' % blog_pk, 'true')
    return response


def archives(request, year, month):
    blog_lists = Blog.objects.filter(created_time__year=year,
                                     created_time__month=month)
    return render(request, 'blog/list.html', context={'blog_lists': blog_lists})


def category(request, category_pk):
    cate = get_object_or_404(Category, pk=category_pk)
    blog_lists = Blog.objects.filter(category=cate)
    return render(request, 'blog/list.html', context={'blog_lists': blog_lists})

