from django.conf.urls import url

from booktest import views

urlpatterns = [
    url('^index/$',views.IndexView.as_view()),
    # url('^book/$',views.BookView.as_view()),
    url(r'^books/$', views.BooksAPIVIew.as_view()),
    url(r'^books/(?P<pk>\d+)/$', views.BookAPIView.as_view())
]