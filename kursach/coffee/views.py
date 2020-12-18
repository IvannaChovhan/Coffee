import json
import plotly.express as px
from django.http import HttpResponseRedirect, QueryDict, HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate
from django.core.paginator import Paginator
from django.apps import apps
# Create your views here.
from django.urls import reverse
import plotly.offline as py

from .forms import *
import csv
import io
import pandas as pd


def get_data_frame_data(Model):
    return pd.DataFrame(Model.objects.all().values())


def top_buyers_by_amount(data):
    top_buyers_by_price = data[data['purchase'] == 'BUY'].groupby('nameBuyer')['price'] \
        .sum().sort_values(ascending=False).head(10)
    df = top_buyers_by_price.reset_index()
    df.columns = ['Name', 'Amount']
    fig = px.bar(data_frame=df, x='Amount', y='Name',
                 color='Amount', orientation='h', color_discrete_sequence=px.colors.sequential.Viridis)
    fig.update_traces(hovertemplate='%{y}<br>$%{x}')
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        yaxis_title='',
        xaxis_title='',
        showlegend=False,
        template='plotly_white'
    )
    return py.plot(fig, output_type='div')


def top_buyers_by_count(data):
    top_buyers_by_count = data[data['purchase'] == 'BUY'].groupby('nameBuyer')['price'] \
        .count().sort_values(ascending=False).head(10)
    df = top_buyers_by_count.reset_index()
    df.columns = ['Name', 'Count']
    fig = px.bar(data_frame=df, y='Name', x='Count', orientation='h',
                 color_discrete_sequence=px.colors.sequential.Cividis, color='Name')
    fig.update_traces(hovertemplate='%{y}<br>Count orders: %{x}')
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        yaxis_title='',
        xaxis_title='',
        showlegend=False,
        template='plotly_white'
    )
    return py.plot(fig, output_type='div')


def count_coffeeTypes_in_orders(data):
    data_coffeeTypes = get_data_frame_data(CoffeeType).set_index('id')
    coffeTypesByOrders = data.join(data_coffeeTypes, on=['coffeeType_id'])[['nameCoffeeType', 'purchase']]
    # print(coffeTypesByOrders.columns)
    coffeTypesByOrders = coffeTypesByOrders[coffeTypesByOrders['purchase'] == 'SELL'].groupby('nameCoffeeType')[
        'nameCoffeeType'] \
        .count().sort_values(ascending=False)
    coffeTypesByOrders.index.names = ['index']
    df = coffeTypesByOrders.reset_index()
    df.columns = ['Name', 'Count']
    fig = px.pie(df, values='Count', names='Name', color_discrete_sequence=['#4e73df', '#36b9cc'],
                 template='plotly_white')
    fig.update_traces(hole=.6, hovertemplate='%{label}: %{value}')
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
    )
    return py.plot(fig, output_type='div')


def profit_by_months(data):
    sell_buy = data
    sell_buy['dateOrder'] = sell_buy['dateOrder'].apply(pd.to_datetime)
    sell_buy = data.set_index('dateOrder')
    Buy = sell_buy[sell_buy['purchase'] == 'BUY']
    Sell = sell_buy[sell_buy['purchase'] == 'SELL']
    Buy = Buy.groupby([lambda x: x.year, lambda x: x.month])['price'].sum()
    Sell = Sell.groupby([lambda x: x.year, lambda x: x.month])['price'].sum()
    res = Sell - Buy
    res = res.reset_index()
    res['date'] = res['level_0'].apply(lambda x: str(x) + '-') + res['level_1'].apply(str)
    res.drop(['level_0', 'level_1'], axis=1, inplace=True)
    res['date'] = res['date'].apply(pd.to_datetime)
    df = res
    df.columns = ['Amount', 'Date']
    annualProfit = df['Amount'].sum()
    fig = px.area(data_frame=df, x='Date', y='Amount')
    fig.update_traces(hovertemplate='%{x}<br>$%{y}', line_shape='spline')
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        yaxis_title='',
        xaxis_title='',
        showlegend=False,
        template='plotly_white'

    )
    return py.plot(fig, output_type='div'), annualProfit


def get_month_profit(data):
    sell_buy = data
    sell_buy['dateOrder'] = sell_buy['dateOrder'].apply(pd.to_datetime)
    sell_buy = data.set_index('dateOrder')
    Buy = sell_buy[sell_buy['purchase'] == 'BUY']
    Sell = sell_buy[sell_buy['purchase'] == 'SELL']
    Buy = Buy.groupby([lambda x: x.year, lambda x: x.month, lambda x: x.day])['price'].sum()
    Sell = Sell.groupby([lambda x: x.year, lambda x: x.month, lambda x: x.day])['price'].sum()
    # print(res)
    Sell = Sell.reset_index()
    Buy = Buy.reset_index()
    Sell['date'] = Sell['level_0'].apply(lambda x: str(x) + '-') + Sell['level_1'].apply(lambda x: str(x) + '-') + Sell[
        'level_2'].apply(str)
    Sell.drop(['level_0', 'level_1', 'level_2'], axis=1, inplace=True)
    Sell['date'] = Sell['date'].apply(pd.to_datetime)
    dateEnd = pd.to_datetime("now")
    dateStart = dateEnd.floor('d') - pd.offsets.Day(30)
    value = Sell.loc[(Sell.date >= dateStart) & (Sell.date <= dateEnd), 'price'].sum()

    Buy['date'] = Buy['level_0'].apply(lambda x: str(x) + '-') + Buy['level_1'].apply(lambda x: str(x) + '-') + Buy[
        'level_2'].apply(str)
    Buy.drop(['level_0', 'level_1', 'level_2'], axis=1, inplace=True)
    Buy['date'] = Buy['date'].apply(pd.to_datetime)
    value2 = Buy.loc[(Buy.date >= dateStart) & (Buy.date <= dateEnd), 'price'].sum()

    return value - value2


def top_products(data):
    sell_buy = data
    Buy = sell_buy[sell_buy['purchase'] == 'BUY']
    Sell = sell_buy[sell_buy['purchase'] == 'SELL']
    res = Sell.groupby('coffeeProduct_id')['price'].sum() - Buy.groupby('coffeeProduct_id')['price'].sum()
    res = res.sort_values(ascending=False).head(10)
    df = res.reset_index()
    df.columns = ['coffeeProduct', 'Amount']
    df['coffeeProduct'] = df['coffeeProduct'].apply(str)
    fig = px.bar(data_frame=df, x='coffeeProduct', y='Amount',
                 color='Amount', color_discrete_sequence=px.colors.sequential.Tealgrn)
    fig.update_traces(hovertemplate='Id: %{x}<br>$%{y}')
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        xaxis=dict(type='category'),
        yaxis_title='',
        xaxis_title='',
        showlegend=False,
        template='plotly_white'
    )
    return py.plot(fig, output_type='div')


def profit_by_harvest_year(data):
    sell_buy = data
    Buy = sell_buy[sell_buy['purchase'] == 'BUY']
    Sell = sell_buy[sell_buy['purchase'] == 'SELL']
    res = Sell.groupby('harvestYear')['price'].sum() - Buy.groupby('harvestYear')['price'].sum()
    res = res.sort_values(ascending=False).head(10)
    df = res.reset_index()
    df.columns = ['harvestYear', 'Amount']
    df['harvestYear'] = df['harvestYear'].apply(int)
    df = df.sort_values('harvestYear')
    print(df)
    fig = px.line(x=df['harvestYear'], y=df['Amount'], color_discrete_sequence=px.colors.sequential.Viridis)
    fig.update_traces(line_shape='spline',  mode='lines+markers', fill='tozeroy', hovertemplate='%{x}<br>$%{y}')
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        yaxis_title='',
        xaxis_title='',
        showlegend=False,
        template='plotly_white'

    )
    return py.plot(fig, output_type='div')


def index(request):
    if request.user.is_authenticated:
        data_orders = get_data_frame_data(Order)
        total_orders = len(data_orders[data_orders['purchase'] == 'SELL'])

        table_coffeeProduct = get_data_frame_data(CoffeeProduct).set_index('id')

        table_buyers = get_data_frame_data(Buyer).set_index('id')
        total_buyers = len(table_buyers)

        joined = data_orders.join(table_coffeeProduct, on=['coffeeProduct_id'])
        joined = joined.join(table_buyers, on=['buyer_id'])
        joined = joined.dropna()

        joined.drop(['phoneNumberBuyer', 'emailBuyer'], axis=1, inplace=True)
        monthProfit = get_month_profit(joined)
        monthProfitGraph, yearProfit = profit_by_months(joined)
        graphs = {'profitMonths': monthProfitGraph,
                  'profitProducts': top_products(joined),
                  'top_buyers': top_buyers_by_amount(joined),
                  'pieCoffeeTypes': count_coffeeTypes_in_orders(joined)
                  }

        context = {'graphs': graphs,
                   'total_orders': total_orders,
                   'monthProfit': monthProfit,
                   'yearProfit': yearProfit,
                   'total_buyers': total_buyers}
        return render(request, 'coffee/index.html', context)
    else:
        return HttpResponseRedirect(reverse('coffee:login'))


def login_view(request):
    title = 'Login'
    error_message = ''
    if request.method == 'POST':
        user = authenticate(request, username=request.POST.get('username'), password=request.POST.get('password'))
        if user is not None:
            # A backend authenticated the credentials
            login(request, user)
            return redirect('coffee:home')
        else:
            error_message = "Login or password are incorrect"
    form = AuthenticationForm()
    context = {
        'title': title,
        'form': form,
        'error': error_message
    }
    return render(request, 'coffee/login.html', context)


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('coffee:login'))


@login_required()
def table_countries_page(request):
    error = {}
    message = ''
    if request.method == 'POST':
        form = CountryForm(request.POST)
        if form.is_valid():
            c, created = Country.objects.get_or_create(**form.cleaned_data)
            if created:
                request.session['message'] = 'Added successful!'
            else:
                request.session['message'] = 'This row already exists'
            return HttpResponseRedirect(reverse('coffee:table_countries'))
            # return HttpResponseRedirect(reverse('coffee:form_owner'))
        else:
            for field in form.errors:
                error[field] = form.errors[field].as_text()

    form = CountryForm()
    fields, page_obj, object_list = get_objects_and_pagination(request, Country, form)
    if request.session.get('message'):
        message = request.session.pop('message')

    context = {
        'title': 'Countries',
        'form': form,
        'errors': error,
        'message': message,
        'page_obj': page_obj,
        'fields': fields,
        'object_list': object_list,
        'model': 'Country',
        'link_upload': 'coffee:upload_csv_countries'
    }
    return render(request, 'coffee/tables_example.html', context)


@login_required()
def table_coffeeType_page(request):
    error = {}
    message = ''
    if request.method == 'POST':
        form = CoffeeTypeForm(request.POST)
        if form.is_valid():
            c, created = CoffeeType.objects.get_or_create(**form.cleaned_data)
            if created:
                request.session['message'] = 'Added successful!'
            else:
                request.session['message'] = 'This row already exists'
            return HttpResponseRedirect(reverse('coffee:table_coffeeTypes'))
            # return HttpResponseRedirect(reverse('coffee:form_owner'))
        else:
            for field in form.errors:
                error[field] = form.errors[field].as_text()

    form = CoffeeTypeForm()
    fields, page_obj, object_list = get_objects_and_pagination(request, CoffeeType, form)
    if request.session.get('message'):
        message = request.session.pop('message')

    context = {
        'title': 'Coffee types',
        'form': form,
        'errors': error,
        'message': message,
        'page_obj': page_obj,
        'fields': fields,
        'object_list': object_list,
        'model': 'CoffeeType',
        'link_upload': 'coffee:upload_csv_coffeetypes'

    }
    return render(request, 'coffee/tables_example.html', context)


@login_required()
def table_buyer_page(request):
    error = {}
    message = ''
    if request.method == 'POST':
        form = BuyerForm(request.POST)
        if form.is_valid():
            c, created = Buyer.objects.get_or_create(**form.cleaned_data)
            if created:
                request.session['message'] = 'Added successful!'
            else:
                request.session['message'] = 'This row already exists'
            return HttpResponseRedirect(reverse('coffee:table_buyers'))
            # return HttpResponseRedirect(reverse('coffee:form_owner'))
        else:
            for field in form.errors:
                error[field] = form.errors[field].as_text()

    form = BuyerForm()
    fields, page_obj, object_list = get_objects_and_pagination(request, Buyer, form)
    if request.session.get('message'):
        message = request.session.pop('message')

    context = {
        'title': 'Buyers',
        'form': form,
        'errors': error,
        'message': message,
        'page_obj': page_obj,
        'fields': fields,
        'object_list': object_list,
        'model': 'Buyer',
        'link_upload': 'coffee:upload_csv_buyer'
    }
    return render(request, 'coffee/tables_example.html', context)


@login_required()
def table_owner_page(request):
    error = {}
    message = ''
    if request.method == 'POST':
        form = OwnerForm(request.POST)
        if form.is_valid():
            c, created = Owner.objects.get_or_create(**form.cleaned_data)
            if created:
                request.session['message'] = 'Added successful!'
            else:
                request.session['message'] = 'This row already exists'
            return HttpResponseRedirect(reverse('coffee:table_owners'))
        else:
            for field in form.errors:
                error[field] = form.errors[field].as_text()

    form = OwnerForm()
    fields, page_obj, object_list = get_objects_and_pagination(request, Owner, form)
    if request.session.get('message'):
        message = request.session.pop('message')
    context = {
        'title': 'Farm owners',
        'object_list': object_list,
        'form': form,
        'errors': error,
        'message': message,
        'page_obj': page_obj,
        'fields': fields,
        'model': 'Owner',
        'link_upload': 'coffee:upload_csv_owner'
    }
    return render(request, 'coffee/tables_example.html', context)


@login_required()
def table_farm_page(request):
    error = {}
    message = ''
    if request.method == 'POST':
        form = FarmForm(request.POST)
        if form.is_valid():
            c, created = Farm.objects.get_or_create(**form.cleaned_data)
            if created:
                request.session['message'] = 'Added successful!'
            else:
                request.session['message'] = 'This row already exists'
            return HttpResponseRedirect(reverse('coffee:table_farms'))
            # return HttpResponseRedirect(reverse('coffee:form_owner'))
        else:
            for field in form.errors:
                error[field] = form.errors[field].as_text()

    form = FarmForm()
    fields, page_obj, object_list = get_objects_and_pagination(request, Farm, form)
    if request.session.get('message'):
        message = request.session.pop('message')

    context = {
        'title': 'Farms',
        'form': form,
        'errors': error,
        'message': message,
        'page_obj': page_obj,
        'fields': fields,
        'object_list': object_list,
        'model': 'Farm',
        'link_upload': 'coffee:upload_csv_farm'
    }
    return render(request, 'coffee/tables_example.html', context)


@login_required()
def table_coffeeProducts_page(request):
    error = {}
    message = ''
    if request.method == 'POST':
        form = CoffeeProductForm(request.POST)
        if form.is_valid():
            c, created = CoffeeProduct.objects.get_or_create(**form.cleaned_data)
            if created:
                request.session['message'] = 'Added successful!'
            else:
                request.session['message'] = 'This row already exists'
            return HttpResponseRedirect(reverse('coffee:table_coffeeProducts'))
            # return HttpResponseRedirect(reverse('coffee:form_owner'))
        else:
            for field in form.errors:
                error[field] = form.errors[field].as_text()

    form = CoffeeProductForm()
    fields, page_obj, object_list = get_objects_and_pagination(request, CoffeeProduct, form)
    if request.session.get('message'):
        message = request.session.pop('message')

    context = {
        'title': 'Coffee products',
        'form': form,
        'errors': error,
        'message': message,
        'page_obj': page_obj,
        'fields': fields,
        'object_list': object_list,
        'model': 'CoffeeProduct',
        'link_upload': 'coffee:upload_csv_coffee_product'
    }
    return render(request, 'coffee/tables_example.html', context)


@login_required()
def table_certificate_page(request):
    error = {}
    message = ''
    if request.method == 'POST':
        form = CertificateForm(request.POST)
        if form.is_valid():
            c, created = Certificate.objects.get_or_create(**form.cleaned_data)
            if created:
                request.session['message'] = 'Added successful!'
            else:
                request.session['message'] = 'This row already exists'
            return HttpResponseRedirect(reverse('coffee:table_certificates'))
            # return HttpResponseRedirect(reverse('coffee:form_owner'))
        else:
            for field in form.errors:
                error[field] = form.errors[field].as_text()

    form = CertificateForm()
    fields, page_obj, object_list = get_objects_and_pagination(request, Certificate, form)
    if request.session.get('message'):
        message = request.session.pop('message')
    context = {
        'title': 'Certificates',
        'form': form,
        'errors': error,
        'message': message,
        'page_obj': page_obj,
        'fields': fields,
        'object_list': object_list,
        'model': 'Certificate',
        'link_upload': 'coffee:upload_csv_certificate'
    }
    return render(request, 'coffee/tables_example.html', context)


@login_required()
def table_order_page(request):
    error = {}
    message = ''
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            c, created = Order.objects.get_or_create(**form.cleaned_data)
            if created:
                request.session['message'] = 'Added successful!'
            else:
                request.session['message'] = 'This row already exists'
            return HttpResponseRedirect(reverse('coffee:table_orders'))
            # return HttpResponseRedirect(reverse('coffee:form_owner'))
        else:
            for field in form.errors:
                error[field] = form.errors[field].as_text()

    form = OrderForm()
    fields, page_obj, object_list = get_objects_and_pagination(request, Order, form)
    if request.session.get('message'):
        message = request.session.pop('message')

    context = {
        'title': 'Orders',
        'form': form,
        'errors': error,
        'message': message,
        'page_obj': page_obj,
        'fields': fields,
        'object_list': object_list,
        'model': 'Order',
        'link_upload': 'coffee:upload_csv_order'
    }
    return render(request, 'coffee/tables_example.html', context)


@login_required()
def table_payment_page(request):
    error = {}
    message = ''
    if request.method == 'POST':
        form = PaymentForm(request.POST)
        if form.is_valid():
            c, created = Payment.objects.get_or_create(**form.cleaned_data)
            if created:
                request.session['message'] = 'Added successful!'
            else:
                request.session['message'] = 'This row already exists'
            return HttpResponseRedirect(reverse('coffee:table_payments'))
            # return HttpResponseRedirect(reverse('coffee:form_owner'))
        else:
            for field in form.errors:
                error[field] = form.errors[field].as_text()

    form = PaymentForm()
    fields, page_obj, object_list = get_objects_and_pagination(request, Payment, form)
    if request.session.get('message'):
        message = request.session.pop('message')

    context = {
        'title': 'Payments',
        'form': form,
        'errors': error,
        'message': message,
        'page_obj': page_obj,
        'fields': fields,
        'object_list': object_list,
        'model': 'Payment',
        'link_upload': 'coffee:upload_csv_payment'
    }
    return render(request, 'coffee/tables_example.html', context)


def get_objects_and_pagination(request, model, form):
    """
    :param request: 
    :param model: like Owner or Farm
    :param form: form of its model
    :return: 
    """""
    fields = ['Id']
    for field in form:
        fields.append(str(field.label))
    model_list = model.objects.get_queryset().order_by('id').reverse()
    object_list = [obj.get_values() for obj in model_list]
    return fields, model_list, object_list


def delete_row(request):
    if request.method == 'DELETE':
        model = apps.get_model('coffee', QueryDict(request.body).get('model'))
        row = model.objects.get(pk=int(QueryDict(request.body).get('id')))
        row.delete()
        data = {
            'deleted': True,
        }
        return JsonResponse(data)


def update_row(request, model, id):
    error = {}
    message = ''
    modelform = eval(model + 'Form')
    model = apps.get_model('coffee', model)

    row = model.objects.get(pk=id)
    if not request.session.get('prev_link'):
        request.session['prev_link'] = request.META.get('HTTP_REFERER')
    prev_link = request.META.get('HTTP_REFERER')
    if request.method == 'POST':
        form = modelform(request.POST)
        if form.is_valid():
            model.objects.filter(pk=id).update(**form.cleaned_data)
            updated = model.objects.get(**form.cleaned_data)
            prev_link = request.session.pop('prev_link')
            if updated:
                request.session['message'] = 'Updated successful!'
            else:
                request.session['message'] = 'This row already exists'
        else:
            for field in form.errors:
                error[field] = form.errors[field].as_text()

    init_dict = {}
    form = modelform()
    for field in form.fields:
        init_dict[field] = row._meta.get_field(field).value_from_object(row)

    if request.session.get('message'):
        message = request.session.pop('message')

    form = modelform(initial=init_dict)

    context = {
        'title': 'Update table',
        'form': form,
        'errors': error,
        'message': message,
        'prev_link': prev_link
    }
    return render(request, 'coffee/form.html', context)


@login_required()
def upload_csv_countries(request):
    template = 'coffee/upload_file.html'
    message = ''
    title = 'Upload csv for countries'
    if request.method == "GET":
        context = {
            'title': title,
            'message': message
        }
        return render(request, template, context)

    csv_file = request.FILES['file']

    if not csv_file.name.endswith('.csv'):
        message = "This is not csv file"
    else:
        data_set = csv_file.read().decode('UTF-8')
        io_string = io.StringIO(data_set)

        next(io_string)
        for column in csv.reader(io_string, delimiter=',', quotechar='|'):
            _, created = Country.objects.update_or_create(
                nameCountry=column[0]
            )

    context = {
        'title': title,
        'message': message
    }
    return render(request, template, context)


@login_required()
def upload_csv_coffeetypes(request):
    template = 'coffee/upload_file.html'
    message = ''
    title = 'Upload csv for coffee types'
    if request.method == "GET":
        context = {
            'title': title,
            'message': message
        }
        return render(request, template, context)

    csv_file = request.FILES['file']

    if not csv_file.name.endswith('.csv'):
        message = "This is not csv file"
    else:
        data_set = csv_file.read().decode('UTF-8')
        io_string = io.StringIO(data_set)

        next(io_string)
        for column in csv.reader(io_string, delimiter=',', quotechar='|'):
            _, created = CoffeeType.objects.update_or_create(
                nameCoffeeType=column[0]
            )

    context = {
        'title': title,
        'message': message
    }
    return render(request, template, context)


@login_required()
def upload_csv_buyer(request):
    template = 'coffee/upload_file.html'
    message = ''
    title = 'Upload csv for buyers'
    if request.method == "GET":
        context = {
            'title': title,
            'message': message
        }
        return render(request, template, context)

    csv_file = request.FILES['file']

    if not csv_file.name.endswith('.csv'):
        message = "This is not csv file"
    else:
        data_set = csv_file.read().decode('UTF-8')
        io_string = io.StringIO(data_set)

        next(io_string)
        for column in csv.reader(io_string, delimiter=',', quotechar='|'):
            _, created = Buyer.objects.update_or_create(
                nameBuyer=column[0],
                phoneNumberBuyer=column[1],
                emailBuyer=column[2]
            )

    context = {
        'title': title,
        'message': message
    }
    return render(request, template, context)


@login_required()
def upload_csv_owner(request):
    template = 'coffee/upload_file.html'
    message = ''
    title = 'Upload csv for owners'
    if request.method == "GET":
        context = {
            'title': title,
            'message': message
        }
        return render(request, template, context)

    csv_file = request.FILES['file']

    if not csv_file.name.endswith('.csv'):
        message = "This is not csv file"
    else:
        data_set = csv_file.read().decode('UTF-8')
        io_string = io.StringIO(data_set)

        next(io_string)
        for column in csv.reader(io_string, delimiter=',', quotechar='|'):
            _, created = Owner.objects.update_or_create(
                nameOwner=column[0],
                phoneNumberOwner=column[1],
                emailOwner=column[2]
            )

    context = {
        'title': title,
        'message': message
    }
    return render(request, template, context)


@login_required()
def upload_csv_farm(request):
    template = 'coffee/upload_file.html'
    message = ''
    title = 'Upload csv for farms'
    if request.method == "GET":
        context = {
            'title': title,
            'message': message
        }
        return render(request, template, context)

    csv_file = request.FILES['file']

    if not csv_file.name.endswith('.csv'):
        message = "This is not csv file"
    else:
        data_set = csv_file.read().decode('UTF-8')
        io_string = io.StringIO(data_set)

        next(io_string)
        for column in csv.reader(io_string, delimiter=',', quotechar='|'):
            _, created = Farm.objects.update_or_create(
                nameFarm=column[0],
                ownerFarm=Owner.objects.get(id=int(column[1])),
                countryFarm=Country.objects.get(id=int(column[2]))
            )

    context = {
        'title': title,
        'message': message
    }
    return render(request, template, context)


@login_required()
def upload_csv_coffee_product(request):
    template = 'coffee/upload_file.html'
    message = ''
    title = 'Upload csv for coffee products'
    if request.method == "GET":
        context = {
            'title': title,
            'message': message
        }
        return render(request, template, context)

    csv_file = request.FILES['file']

    if not csv_file.name.endswith('.csv'):
        message = "This is not csv file"
    else:
        data_set = csv_file.read().decode('UTF-8')
        io_string = io.StringIO(data_set)

        next(io_string)
        for column in csv.reader(io_string, delimiter=',', quotechar='|'):
            _, created = CoffeeProduct.objects.update_or_create(
                coffeeType=CoffeeType.objects.get(id=column[0]),
                harvestYear=column[1],
                farm=Farm.objects.get(id=column[2]),
                aroma=column[3],
                aftertaste=column[4],
                flavor=column[5],
                color=column[6]
            )

    context = {
        'title': title,
        'message': message
    }
    return render(request, template, context)


@login_required()
def upload_csv_certificate(request):
    template = 'coffee/upload_file.html'
    message = ''
    title = 'Upload csv for certificates'
    if request.method == "GET":
        context = {
            'title': title,
            'message': message
        }
        return render(request, template, context)

    csv_file = request.FILES['file']

    if not csv_file.name.endswith('.csv'):
        message = "This is not csv file"
    else:
        data_set = csv_file.read().decode('UTF-8')
        io_string = io.StringIO(data_set)

        next(io_string)
        for column in csv.reader(io_string, delimiter=',', quotechar='|'):
            _, created = Certificate.objects.update_or_create(
                body=column[0],
                product=CoffeeProduct(id=column[1]),
                dateOfExpire=column[2],
                disadvantages=column[3]
            )

    context = {
        'title': title,
        'message': message
    }
    return render(request, template, context)


@login_required()
def upload_csv_order(request):
    template = 'coffee/upload_file.html'
    message = ''
    title = 'Upload csv for orders'
    if request.method == "GET":
        context = {
            'title': title,
            'message': message
        }
        return render(request, template, context)

    csv_file = request.FILES['file']

    if not csv_file.name.endswith('.csv'):
        message = "This is not csv file"
    else:
        data_set = csv_file.read().decode('UTF-8')
        io_string = io.StringIO(data_set)

        next(io_string)
        for column in csv.reader(io_string, delimiter=',', quotechar='|'):
            _, created = Order.objects.update_or_create(
                coffeeProduct=CoffeeProduct.objects.get(id=column[0]),
                weight=column[1],
                price=column[2],
                dateOrder=column[3],
                buyer=Buyer.objects.get(id=column[4]),
                purchase=column[5]
            )

    context = {
        'title': title,
        'message': message
    }
    return render(request, template, context)


@login_required()
def upload_csv_payment(request):
    template = 'coffee/upload_file.html'
    message = ''
    title = 'Upload csv for payments'
    if request.method == "GET":
        context = {
            'title': title,
            'message': message
        }
        return render(request, template, context)

    csv_file = request.FILES['file']

    if not csv_file.name.endswith('.csv'):
        message = "This is not csv file"
    else:
        data_set = csv_file.read().decode('UTF-8')
        io_string = io.StringIO(data_set)

        next(io_string)
        for column in csv.reader(io_string, delimiter=',', quotechar='|'):
            _, created = Payment.objects.update_or_create(
                order=Order.objects.get(id=column[0]),
                datePayment=column[1],
                amount=column[2]
            )

    context = {
        'title': title,
        'message': message
    }
    return render(request, template, context)


@login_required()
def report_order(request):
    error = {}
    message = ''
    template = 'coffee/report.html'
    table = ''
    date = []
    if request.method == 'POST':
        form = DateForm(request.POST)
        if form.is_valid():
            data_orders = get_data_frame_data(Order)
            data_orders['dateOrder'] = data_orders['dateOrder'].apply(pd.to_datetime)
            date_end = pd.to_datetime(form.cleaned_data.get('date_end'))
            date_start = pd.to_datetime(form.cleaned_data.get('date_begin'))
            date = [date_start.year, date_start.month, date_start.day, date_end.year, date_end.month, date_end.day]
            print(date)
            table = data_orders.loc[(data_orders['dateOrder'] >= date_start) & (data_orders['dateOrder'] <= date_end)]
            table = table.sort_values(by=['dateOrder']).to_html(classes='table table-bordered', index=False)

        else:
            for field in form.errors:
                error[field] = form.errors[field].as_text()

    form = DateForm()

    context = {
        'title': 'Order report',
        'form': form,
        'errors': error,
        'message': message,
        'table': table,
        'csv': True,
        'date': date,
        'flag': 'all'
    }
    return render(request, template, context)


@login_required()
def report_sell(request):
    error = {}
    message = ''
    template = 'coffee/report.html'
    table = ''
    date = []
    if request.method == 'POST':
        form = DateForm(request.POST)
        if form.is_valid():
            data_orders = get_data_frame_data(Order)
            data_orders['dateOrder'] = data_orders['dateOrder'].apply(pd.to_datetime)
            data_orders = data_orders[data_orders['purchase'] == 'SELL']
            date_end = pd.to_datetime(form.cleaned_data.get('date_end'))
            date_start = pd.to_datetime(form.cleaned_data.get('date_begin'))
            date = [date_start.year, date_start.month, date_start.day, date_end.year, date_end.month, date_end.day]
            print(date)
            table = data_orders.loc[(data_orders['dateOrder'] >= date_start) & (data_orders['dateOrder'] <= date_end)]
            table = table.sort_values(by=['dateOrder']).to_html(classes='table table-bordered', index=False)

        else:
            for field in form.errors:
                error[field] = form.errors[field].as_text()

    form = DateForm()

    context = {
        'title': 'Sell report',
        'form': form,
        'errors': error,
        'message': message,
        'table': table,
        'csv': True,
        'date': date,
        'flag': 'sell'
    }
    return render(request, template, context)


@login_required()
def report_buy(request):
    error = {}
    message = ''
    template = 'coffee/report.html'
    table = ''
    date = []
    if request.method == 'POST':
        form = DateForm(request.POST)
        if form.is_valid():
            data_orders = get_data_frame_data(Order)
            data_orders['dateOrder'] = data_orders['dateOrder'].apply(pd.to_datetime)
            data_orders = data_orders[data_orders['purchase'] == 'BUY']
            date_end = pd.to_datetime(form.cleaned_data.get('date_end'))
            date_start = pd.to_datetime(form.cleaned_data.get('date_begin'))
            date = [date_start.year, date_start.month, date_start.day, date_end.year, date_end.month, date_end.day]
            print(date)
            table = data_orders.loc[(data_orders['dateOrder'] >= date_start) & (data_orders['dateOrder'] <= date_end)]
            table = table.sort_values(by=['dateOrder']).to_html(classes='table table-bordered', index=False)

        else:
            for field in form.errors:
                error[field] = form.errors[field].as_text()

    form = DateForm()

    context = {
        'title': 'Buy report',
        'form': form,
        'errors': error,
        'message': message,
        'table': table,
        'csv': True,
        'date': date,
        'flag': 'buy'
    }
    return render(request, template, context)


@login_required()
def charts_page(request):
    data_orders = get_data_frame_data(Order)
    table_coffeeProduct = get_data_frame_data(CoffeeProduct).set_index('id')
    table_buyers = get_data_frame_data(Buyer).set_index('id')

    joined = data_orders.join(table_coffeeProduct, on=['coffeeProduct_id'])
    joined = joined.join(table_buyers, on=['buyer_id'])
    joined = joined.dropna()

    joined.drop(['phoneNumberBuyer', 'emailBuyer'], axis=1, inplace=True)

    monthProfitGraph, yearProfit = profit_by_months(joined)

    graphs = {'profitMonths': monthProfitGraph,
              'profitProducts': top_products(joined),
              'top_buyers': top_buyers_by_amount(joined),
              'pieCoffeeTypes': count_coffeeTypes_in_orders(joined),
              'topBuyersCountGraph': top_buyers_by_count(joined),
              'profitHarvestYearGraph': profit_by_harvest_year(joined)
              }

    context = {'graphs': graphs}

    return render(request, 'coffee/charts.html', context)


@login_required()
def report_deptors(request):
    template = 'coffee/report.html'

    data_orders = get_data_frame_data(Order).set_index('id')

    table_payments = get_data_frame_data(Payment).set_index('id')

    table_buyers = get_data_frame_data(Buyer).set_index('id')

    table_payments = table_payments.join(data_orders, on=['order_id'])
    table_payments = table_payments[table_payments['purchase'] == 'BUY']
    table_payments['diff'] = table_payments['price'] - table_payments['amount']
    table_payments = table_payments[table_payments['diff'] > 0]
    table_payments = table_payments.join(table_buyers, on=['buyer_id'])


    context = {
        'title': 'Deptors report',
        'table': table_payments[['order_id', 'nameBuyer', 'diff']].to_html(classes='table table-bordered', index=False),
        'csv': True
    }
    return render(request, template, context)


@login_required()
def export_csv(request, first_year, first_month, first_day, end_year, end_month, end_day, flag):
    data_orders = get_data_frame_data(Order)
    data_orders['dateOrder'] = data_orders['dateOrder'].apply(pd.to_datetime)
    if flag == 'sell':
        data_orders = data_orders[data_orders['purchase'] == 'SELL']
    elif flag == 'buy':
        data_orders = data_orders[data_orders['purchase'] == 'BUY']
    date_start = pd.to_datetime(str(first_year) + '-' + str(first_month) + '-' + str(first_day))
    date_end = pd.to_datetime(str(end_year) + '-' + str(end_month) + '-' + str(end_day))
    table = data_orders.loc[(data_orders['dateOrder'] >= date_start) & (data_orders['dateOrder'] <= date_end)]
    table = table.sort_values(by=['dateOrder'])
    response = HttpResponse(table.to_csv(encoding='utf-8', index=False), content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="export.csv"'
    return response


@login_required()
def export_csv_deptors(request):
    data_orders = get_data_frame_data(Order).set_index('id')

    table_payments = get_data_frame_data(Payment).set_index('id')

    table_buyers = get_data_frame_data(Buyer).set_index('id')

    table_payments = table_payments.join(data_orders, on=['order_id'])
    table_payments = table_payments[table_payments['purchase'] == 'BUY']
    table_payments['diff'] = table_payments['price'] - table_payments['amount']
    table_payments = table_payments[table_payments['diff'] > 0]
    table_payments = table_payments.join(table_buyers, on=['buyer_id'])

    table = table_payments[['order_id', 'nameBuyer', 'diff']]

    response = HttpResponse(table.to_csv(encoding='utf-8', index=False), content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="deptors.csv"'
    return response
