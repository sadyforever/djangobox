# from django.core.urlresolvers import reverse


from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from django.urls import reverse


def index(request):
    '''
    首页视图
    :param request:django框架视图函数结构必有request参数
    :return: 响应内容是由HttpResponse对象给出的
    '''
    request.session['user_name'] = 100
    request.session['user_id'] = 7
    print(reverse('index'))  # /users/index
    return HttpResponse('hello world')