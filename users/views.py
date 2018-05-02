from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.


def index(request):
    '''
    首页视图
    :param request:django框架视图函数结构必有request参数
    :return: 响应内容是由HttpResponse对象给出的
    '''
    return HttpResponse('hello world')