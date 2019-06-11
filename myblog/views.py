from django.shortcuts import render, redirect
from django.contrib import auth


def index(request):
    return render(request, 'index.html', context={
        'title': "我的博客！",
        'welcome': "欢迎来到我的博客！"
    })


def login(request):
    username = request.POST.get('username', '')
    password = request.POST.get('password', '')
    user = auth.authenticate(request, username=username, password=password)
    referer = request.META.get('HTTP_REFERER', '/')
    if user is not None:
        auth.login(request, user)
        return redirect(referer)
    else:
        return render(request, 'error.html', {'message': '用户名或密码错误！'})
