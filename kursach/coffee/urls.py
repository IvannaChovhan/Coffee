from django.urls import path
from django.conf.urls import url
from . import views

app_name = 'coffee'
urlpatterns = [
    path('', views.index, name='home'),
    path('login', views.login_view, name='login'),
    path('logout', views.logout_view, name='logout'),
    path('charts', views.charts_page, name='charts'),
    path('table_countries', views.table_countries_page, name='table_countries'),
    path('table_owners', views.table_owner_page, name='table_owners'),
    path('table_coffeeTypes', views.table_coffeeType_page, name='table_coffeeTypes'),
    path('table_buyers', views.table_buyer_page, name='table_buyers'),
    path('table_farms', views.table_farm_page, name='table_farms'),
    path('table_coffeeProducts', views.table_coffeeProducts_page, name='table_coffeeProducts'),
    path('table_certificates', views.table_certificate_page, name='table_certificates'),
    path('table_orders', views.table_order_page, name='table_orders'),
    path('table_payments', views.table_payment_page, name='table_payments'),
    path('delete_row', views.delete_row, name='delete_row'),
    path(r'<str:model>/<int:id>/update', views.update_row, name='update_row'),
    path('upload_csv_countries', views.upload_csv_countries, name='upload_csv_countries'),
    path('upload_csv_coffeetypes', views.upload_csv_coffeetypes, name='upload_csv_coffeetypes'),
    path('upload_csv_buyer', views.upload_csv_buyer, name='upload_csv_buyer'),
    path('upload_csv_owner', views.upload_csv_owner, name='upload_csv_owner'),
    path('upload_csv_farm', views.upload_csv_farm, name='upload_csv_farm'),
    path('upload_csv_coffee_product', views.upload_csv_coffee_product, name='upload_csv_coffee_product'),
    path('upload_csv_certificate', views.upload_csv_certificate, name='upload_csv_certificate'),
    path('upload_csv_order', views.upload_csv_order, name='upload_csv_order'),
    path('upload_csv_payment', views.upload_csv_payment, name='upload_csv_payment'),
    path('report_order', views.report_order, name='report_order'),
]