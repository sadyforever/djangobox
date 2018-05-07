from django.shortcuts import render

# Create your views here.
from django.views import View


class IndexView(View):

    def get(self,request):
        content = {'city':'北京'}
        return render(request,'index.html',content)

from django.shortcuts import render
from django.views.generic import View
from django.http import HttpResponse

from forms import BookForm

class BookView(View):
    def get(self, request):
        form = BookForm()
        return render(request, 'book.html', {'form': form})

    def post(self, request):
        form = BookForm(request.POST)
        if form.is_valid():  # 验证表单数据
            print(form.cleaned_data)  # 获取验证后的表单数据
            return HttpResponse("OK")
        else:
            return render(request, 'book.html', {'form': form})