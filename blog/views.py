from django.shortcuts import render, get_object_or_404

from .models import Blog, Category


def blog_list(request):
    blogs = Blog.objects.all()
    return render(request, 'blog/list.html', context={
        'blogs': blogs,
    })


def blog_detail(request, blog_pk):
    blog = get_object_or_404(Blog, pk=blog_pk)
    if not request.COOKIES.get('blog_%s_readed' % blog_pk):
        blog.views += 1
        blog.save()
    response = render(request, 'blog/detail.html', context={'blog': blog})
    response.set_cookie('blog_%s_readed' % blog_pk, 'true')
    return response


def archives(request, year, month):
    date_list = Blog.objects.filter(created_time__year=year,
                                    created_time__month=month)
    return render(request, 'blog/list.html', context={'date_list': date_list})


def category(request, category_pk):
    cate = get_object_or_404(Category, pk=category_pk)
    category_list = Blog.objects.filter(category=cate)
    return render(request, 'blog/list.html', context={'category_list': category_list})

