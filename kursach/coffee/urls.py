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
    path('table_coffeeTypes', views.table_coffeeType_page, name='table_coffeeTypes'),
    path('table_buyers', views.table_buyer_page, name='table_buyers'),
    path('table_farms', views.table_farm_page, name='table_farms'),
    path('table_coffeeProducts', views.table_coffeeProducts_page, name='table_coffeeProducts'),
    path('table_certificates', views.table_certificate_page, name='table_certificates'),
    path('table_orders', views.table_order_page, name='table_orders'),
    path('table_payments', views.table_payment_page, name='table_payments'),
    path('delete_row', views.delete_row, name='delete_row')
    #path('form_owner', views.form_owner, name='form_owner'),
]