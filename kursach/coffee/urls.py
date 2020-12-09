from django.urls import path
from django.conf.urls import url
from . import views

app_name = 'coffee'
urlpatterns = [
    path('', views.index, name='home'),
    path('table_countries', views.table_countries_page, name='table_countries'),
    path('table_owners', views.table_owner_page, name='table_owners'),
    path('add_row_owner', views.form_owner, name='add_row_owner'),
]