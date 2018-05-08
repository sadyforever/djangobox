import json
from django.shortcuts import render

# Create your views here.
from django.views import View

from booktest.models import BookInfo, HeroInfo


class IndexView(View):

    def get(self,request):
        content = {'city':'北京'}
        return render(request,'index.html',content)

from django.shortcuts import render
from django.views.generic import View
from django.http import HttpResponse, JsonResponse

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




from datetime import datetime

class BooksAPIVIew(View):
    """
    查询所有图书、增加图书
    """
    def get(self, request):
        """
        查询所有图书
        路由：GET /books/
        """
        queryset = BookInfo.objects.all()
        book_list = []
        for book in queryset:
            book_list.append({
                'id': book.id,
                'btitle': book.btitle,
                'bpub_date': book.bpub_date,
                'bread': book.bread,
                'bcomment': book.bcomment,
                'image': book.image.url if book.image else ''
            })
        return JsonResponse(book_list, safe=False)
        # 对safe的说明,我们传过去的book_list是一个list格式
        # 在前端json支持{}格式也支持[]格式
        # 但是django中认为[]的json格式是不安全的会进行校验
        # 所以把safe选项关闭False,不进行校验就可以传[]



    def post(self, request):
        """
        新增图书
        路由：POST /books/
        """
        json_bytes = request.body
        json_str = json_bytes.decode()
        book_dict = json.loads(json_str)

        # 此处详细的校验参数省略

        book = BookInfo.objects.create(
            btitle=book_dict.get('btitle'),
            bpub_date=datetime.strptime(book_dict.get('bpub_date'), '%Y-%m-%d').date()
        )
            # 使用datetime模块中的strptime方法,把时间 '1990-1-1' 格式的字符串转换成


        return JsonResponse({
            'id': book.id,
            'btitle': book.btitle,
            'bpub_date': book.bpub_date,
            'bread': book.bread,
            'bcomment': book.bcomment,
            'image': book.image.url if book.image else ''
        }, status=201)


class BookAPIView(View):
    def get(self, request, pk):
        """
        获取单个图书信息
        路由： GET  /books/<pk>/
        """
        try:
            book = BookInfo.objects.get(pk=pk)
        except BookInfo.DoesNotExist:
            return HttpResponse(status=404)

        return JsonResponse({
            'id': book.id,
            'btitle': book.btitle,
            'bpub_date': book.bpub_date,
            'bread': book.bread,
            'bcomment': book.bcomment,
            'image': book.image.url if book.image else ''
        })

    def put(self, request, pk):
        """
        修改图书信息
        路由： PUT  /books/<pk>
        """
        try:
            book = BookInfo.objects.get(pk=pk)
        except BookInfo.DoesNotExist:
            return HttpResponse(status=404)

        json_bytes = request.body
        json_str = json_bytes.decode()
        book_dict = json.loads(json_str)

        # 此处详细的校验参数省略

        book.btitle = book_dict.get('btitle')
        book.bpub_date = datetime.strptime(book_dict.get('bpub_date'), '%Y-%m-%d').date()
        book.save()

        return JsonResponse({
            'id': book.id,
            'btitle': book.btitle,
            'bpub_date': book.bpub_date,
            'bread': book.bread,
            'bcomment': book.bcomment,
            'image': book.image.url if book.image else ''
        })

    def delete(self, request, pk):
        """
        删除图书
        路由： DELETE /books/<pk>/
        """
        try:
            book = BookInfo.objects.get(pk=pk)
        except BookInfo.DoesNotExist:
            return HttpResponse(status=404)

        book.delete()

        return HttpResponse(status=204)




from rest_framework.viewsets import ModelViewSet
from .serializers import BookInfoSerializer, HeroInfoSerializer
from .models import BookInfo
                        # ModelViewSet
class BookInfoViewSet(ModelViewSet):    # 继承于模型视图集合
    queryset = BookInfo.objects.all()      # 操作数据库由我们来
    serializer_class = BookInfoSerializer   # serializer_class 声明接下来的序列化使用哪个序列化器


class HeroInfoViewSet(ModelViewSet):    # 使用默认的serializer居然也继承这个
    queryset = HeroInfo.objects.all()
    serializer_class = HeroInfoSerializer