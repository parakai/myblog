from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView

import markdown

from .models import Blog, Category


class IndexView(ListView):
    model = Blog
    template_name = 'blog/list.html'
    context_object_name = 'blog_lists'
    paginate_by = 5

    def get_context_data(self, **kwargs):
        # 首先获得父类生成的传递给模板的字典。
        context = super().get_context_data(**kwargs)
        paginator = context.get('paginator')
        page = context.get('page_obj')
        is_paginated = context.get('is_paginated')

        # 调用自己写的 pagination_data 方法获得显示分页导航条需要的数据，见下方。
        pagination_data = self.pagination_data(paginator, page, is_paginated)

        context.update(pagination_data)
        return context

    def pagination_data(self, paginator, page, is_paginated):
        if not is_paginated:
            return {}
        # 获得用户当前请求的页码号
        page_number = page.number
        # 获得分页后的总页数
        total_pages = paginator.num_pages
        # 获取当前页码前后各2页的页码范围
        page_range = list(range(max(page_number-2, 1), page_number)) + \
                     list(range(page_number, min(page_number+2, total_pages)+1))
        # 加上省略页码标记
        if page_range[0] - 1 >= 2:
            page_range.insert(0, '...')
        if paginator.num_pages - page_range[-1] >= 2:
            page_range.append('...')

        # 加上首页和尾页
        if page_range[0] != 1:
            page_range.insert(0, 1)
        if page_range[-1] != paginator.num_pages:
            page_range.append(paginator.num_pages)
        data = {
            'page_range': page_range
        }
        return data

    def pagination_data2(self, paginator, page, is_paginated):
        if not is_paginated:
            return {}
        # 当前页左边连续的页码号，初始值为空
        left = []
        # 当前页右边连续的页码号，初始值为空
        right = []
        # 标示第 1 页页码后是否需要显示省略号
        left_has_more = False
        # 标示最后一页页码前是否需要显示省略号
        right_has_more = False

        # 标示是否需要显示第 1 页的页码号。
        # 因为如果当前页左边的连续页码号中已经含有第 1 页的页码号，此时就无需再显示第 1 页的页码号，
        # 其它情况下第一页的页码是始终需要显示的。
        # 初始值为 False
        first = False

        # 标示是否需要显示最后一页的页码号。
        # 需要此指示变量的理由和上面相同。
        last = False
        # 获得用户当前请求的页码号
        page_number = page.number
        # 获得分页后的总页数
        total_pages = paginator.num_pages

        # 获得整个分页页码列表，比如分了四页，那么就是 [1, 2, 3, 4]
        page_range = paginator.page_range
        if page_number == 1:
            right = page_range[page_number: page_number + 2]
            if right[-1] < total_pages - 1:
                right_has_more = True
            if right[-1] < total_pages:
                last = True
        elif page_number == total_pages:
            left = page_range[(page_number - 3) if (page_number - 3) > 0 else 0:page_number-1]
            if left[0] > 2:
                left_has_more = True
            if left[0] > 1:
                first = True
        else:
            left = page_range[(page_number - 3) if (page_number - 3) > 0 else 0:page_number - 1]
            right = page_range[page_number:page_number + 2]
            if right[-1] < total_pages - 1:
                right_has_more = True
            if right[-1] < total_pages:
                last = True
            # 是否需要显示第 1 页和第 1 页后的省略号
            if left[0] > 2:
                left_has_more = True
            if left[0] > 1:
                first = True
        data = {
            'left': left,
            'right': right,
            'left_has_more': left_has_more,
            'right_has_more': right_has_more,
            'first': first,
            'last': last,
        }
        return data


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
        response.set_cookie('blog_%s_readed' % self.kwargs.get('pk'), 'true')
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
        comments = self.object.get_comments()
        context.update({
            'previous_blog': previous_blog,
            'next_blog': next_blog,
            'comments': comments,
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
