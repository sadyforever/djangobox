from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.


def weather(request,city,year):
    print(city)
    print(year)
    return HttpResponse('OK')