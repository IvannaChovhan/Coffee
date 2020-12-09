from django.urls import path
from django.conf.urls import url
from . import views

app_name = 'coffee'
urlpatterns = [
    path('', views.index, name='home'),
    path('/tables', views.tables, name='tables'),
]