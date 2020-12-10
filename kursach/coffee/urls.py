from django.urls import path
from django.conf.urls import url
from . import views

app_name = 'coffee'
urlpatterns = [
    path('', views.index, name='home'),
    path('login', views.login_view, name='login'),
    path('logout', views.logout_view, name='logout'),
    path('table_countries', views.table_countries_page, name='table_countries'),
    path('table_owners', views.table_owner_page, name='table_owners'),
    #path('form_owner', views.form_owner, name='form_owner'),
]