from django.conf.urls import url

from booktest import views

urlpatterns = [
    url('^index/$',views.IndexView.as_view()),
    url('^book/$',views.BookView.as_view()),
]