from django.conf.urls import url
from rest_framework.routers import DefaultRouter

from booktest import views

urlpatterns = [
    url('^index/$',views.IndexView.as_view()),
    # url('^book/$',views.BookView.as_view()),
    # url(r'^books/$', views.BooksAPIVIew.as_view()),
    # url(r'^books/(?P<pk>\d+)/$', views.BookAPIView.as_view())
]

# DRF框架的路由注册方式
# 实例路由对象
router = DefaultRouter()  # 可以处理视图的路由器
router.register(r'books', views.BookInfoViewSet)  # 向路由器中注册视图集
# DRF的类视图也不使用as_view了,使用register

router.register(r'heros',views.HeroInfoViewSet)

# 最重要的一点把router添加进django的路由urlpatterns中
urlpatterns += router.urls  # 将路由器中的所以路由信息追到到django的路由列表中