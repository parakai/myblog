from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView

import markdown

from .models import Blog, Category


class IndexView(ListView):
    model = Blog
    template_name = 'blog/list.html'
    context_object_name = 'blog_lists'


def blog_list(request):
    blog_lists = Blog.objects.all()
    return render(request, 'blog/list.html', context={
        'blog_lists': blog_lists,
    })


def blog_detail(request, blog_pk):
    blog = get_object_or_404(Blog, pk=blog_pk)
    blog.content = markdown.markdown(blog.content,
                                     extensions=[
                                      'markdown.extensions.extra',
                                      'markdown.extensions.codehilite',
                                      'markdown.extensions.toc',
                                      ])
    if not request.COOKIES.get('blog_%s_readed' % blog_pk):
        blog.views += 1
        blog.save()
    previous_blog = Blog.objects.filter(created_time__gt=blog.created_time).last()
    next_blog = Blog.objects.filter(created_time__lt=blog.created_time).first()
    response = render(request, 'blog/detail.html', context={'blog': blog,
                      'previous_blog': previous_blog, 'next_blog': next_blog})
    response.set_cookie('blog_%s_readed' % blog_pk, 'true')
    return response


class BlogDetailView(DetailView):
    model = Blog
    template_name = 'blog/detail.html'
    context_object_name = 'blog'

    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        if not request.COOKIES.get('blog_%s_readed' % self.kwargs.get('pk')):
            self.object.views += 1
            self.object.save()
        return response

    def get_object(self, queryset=None):
        blog = super().get_object(queryset=None)
        blog.content = markdown.markdown(blog.content, extensions=[
                                          'markdown.extensions.extra',
                                          'markdown.extensions.codehilite',
                                          'markdown.extensions.toc',
                                      ])
        return blog

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        previous_blog = self.object.get_previous_blog()
        next_blog = self.object.get_next_blog()
        context.update({
            'previous_blog': previous_blog,
            'next_blog': next_blog
        })
        return context


def archives(request, year, month):
    blog_lists = Blog.objects.filter(created_time__year=year,
                                     created_time__month=month)
    return render(request, 'blog/list.html', context={'blog_lists': blog_lists})


class ArchivesView(IndexView):
    def get_queryset(self):
        return super().get_queryset().filter(created_time__year=self.kwargs.get('year'),
                                             created_time__month=self.kwargs.get('month'))


def category(request, category_pk):
    cate = get_object_or_404(Category, pk=category_pk)
    blog_lists = Blog.objects.filter(category=cate)
    return render(request, 'blog/list.html', context={'blog_lists': blog_lists})


# class CategoryView(ListView):
#     model = Blog
#     template_name = 'blog/list.html'
#     context_object_name = 'blog_lists'
#
#     def get_queryset(self):
#         cate = get_object_or_404(Category, pk=self.kwargs.get('category_pk'))
#         return super().get_queryset().filter(category=cate)
class CategoryView(IndexView):
    def get_queryset(self):
        cate = get_object_or_404(Category, pk=self.kwargs.get('category_pk'))
        return super().get_queryset().filter(category=cate)
