from django.shortcuts import render


def index(request):
    return render(request, 'index.html', context={
        'title': "我的博客！",
        'welcome': "欢迎来到我的博客！"
    })
