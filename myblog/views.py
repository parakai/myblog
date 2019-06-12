from django.shortcuts import render, redirect, reverse
from django.contrib import auth
from django.contrib.auth.models import User

from .forms import LoginForm, RegisterForm


def index(request):
    return render(request, 'index.html', context={
        'title': "我的博客！",
        'welcome': "欢迎来到我的博客！"
    })


def login(request):
    # username = request.POST.get('username', '')
    # password = request.POST.get('password', '')
    # user = auth.authenticate(request, username=username, password=password)
    # referer = request.META.get('HTTP_REFERER', '/')
    # if user is not None:
    #     auth.login(request, user)
    #     return redirect(referer)
    # else:
    #     return render(request, 'error.html', {'message': '用户名或密码错误！'})
    if request.method == 'POST':
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            user = login_form.cleaned_data['user']
            auth.login(request, user)
            return redirect(request.GET.get('from', reverse('index')))
    else:
        login_form = LoginForm()
    return render(request, 'login.html', {'login_form': login_form})


def register(request):
    if request.method == 'POST':
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            username = register_form.cleaned_data['username']
            password = register_form.cleaned_data['password']
            email = register_form.cleaned_data['email']
            # 创建用户
            # user = User.objects.create_user(username, password, email)
            # user.save()

            # 另一种实例化User方法
            user = User()
            user.username = username
            user.email = email
            user.set_password(password)
            user.save()
            # 登录
            user = auth.authenticate(username=username, password=password)
            auth.login(request, user)
            return redirect(request.GET.get('from', reverse('index')))
    else:
        register_form = RegisterForm()
    return render(request, 'register.html', {'register_form': register_form})
