import json

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
from .forms import *


def index(request):
    if request.user.is_authenticated:
        return render(request, 'coffee/index.html')
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
            form.save()
            message = 'Added successful!'
            # return HttpResponseRedirect(reverse('coffee:form_owner'))
        else:
            for field in form.errors:
                error[field] = form.errors[field].as_text()

    form = CountryForm()
    fields, page_obj, object_list = get_objects_and_pagination(request, Country, form)

    context = {
        'title': 'Countries',
        'form': form,
        'errors': error,
        'message': message,
        'page_obj': page_obj,
        'fields': fields,
        'object_list': object_list,
        'model': 'Country'
    }
    return render(request, 'coffee/tables_example.html', context)


@login_required()
def table_coffeeType_page(request):
    error = {}
    message = ''
    if request.method == 'POST':
        form = CoffeeTypeForm(request.POST)
        if form.is_valid():
            form.save()
            message = 'Added successful!'
            # return HttpResponseRedirect(reverse('coffee:form_owner'))
        else:
            for field in form.errors:
                error[field] = form.errors[field].as_text()

    form = CoffeeTypeForm()
    fields, page_obj, object_list = get_objects_and_pagination(request, CoffeeType, form)

    context = {
        'title': 'Coffee types',
        'form': form,
        'errors': error,
        'message': message,
        'page_obj': page_obj,
        'fields': fields,
        'object_list': object_list,
        'model': 'CoffeeType'
    }
    return render(request, 'coffee/tables_example.html', context)


@login_required()
def table_buyer_page(request):
    error = {}
    message = ''
    if request.method == 'POST':
        form = BuyerForm(request.POST)
        if form.is_valid():
            form.save()
            message = 'Added successful!'
            # return HttpResponseRedirect(reverse('coffee:form_owner'))
        else:
            for field in form.errors:
                error[field] = form.errors[field].as_text()

    form = BuyerForm()
    fields, page_obj, object_list = get_objects_and_pagination(request, Buyer, form)

    context = {
        'title': 'Buyers',
        'form': form,
        'errors': error,
        'message': message,
        'page_obj': page_obj,
        'fields': fields,
        'object_list': object_list,
        'model': 'Buyer'
    }
    return render(request, 'coffee/tables_example.html', context)


@login_required()
def table_owner_page(request):
    error = {}
    message = ''
    if request.method == 'POST':
        form = OwnerForm(request.POST)
        if form.is_valid():
            form.save()
            message = 'Added successful!'
            #return HttpResponseRedirect(reverse('coffee:form_owner'))
        else:
            for field in form.errors:
                error[field] = form.errors[field].as_text()

    form = OwnerForm()
    fields, page_obj, object_list = get_objects_and_pagination(request, Owner, form)

    context = {
        'title': 'Farm owners',
        'object_list': object_list,
        'form': form,
        'errors': error,
        'message': message,
        'page_obj': page_obj,
        'fields': fields,
        'model': 'Owner'
    }
    return render(request, 'coffee/tables_example.html', context)


@login_required()
def table_farm_page(request):
    error = {}
    message = ''
    if request.method == 'POST':
        form = FarmForm(request.POST)
        if form.is_valid():
            form.save()
            message = 'Added successful!'
            #return HttpResponseRedirect(reverse('coffee:form_owner'))
        else:
            for field in form.errors:
                error[field] = form.errors[field].as_text()

    form = FarmForm()
    fields, page_obj, object_list = get_objects_and_pagination(request, Farm, form)

    context = {
        'title': 'Farms',
        'form': form,
        'errors': error,
        'message': message,
        'page_obj': page_obj,
        'fields': fields,
        'object_list': object_list,
        'model': 'Farm'
    }
    return render(request, 'coffee/tables_example.html', context)


@login_required()
def table_coffeeProducts_page(request):
    error = {}
    message = ''
    if request.method == 'POST':
        form = CoffeeProductForm(request.POST)
        if form.is_valid():
            form.save()
            message = 'Added successful!'
            #return HttpResponseRedirect(reverse('coffee:form_owner'))
        else:
            for field in form.errors:
                error[field] = form.errors[field].as_text()

    form = CoffeeProductForm()
    fields, page_obj, object_list = get_objects_and_pagination(request, CoffeeProduct, form)

    context = {
        'title': 'Coffee products',
        'form': form,
        'errors': error,
        'message': message,
        'page_obj': page_obj,
        'fields': fields,
        'object_list': object_list,
        'model': 'CoffeeProduct'
    }
    return render(request, 'coffee/tables_example.html', context)


@login_required()
def table_certificate_page(request):
    error = {}
    message = ''
    if request.method == 'POST':
        form = CertificateForm(request.POST)
        if form.is_valid():
            form.save()
            message = 'Added successful!'
            #return HttpResponseRedirect(reverse('coffee:form_owner'))
        else:
            for field in form.errors:
                error[field] = form.errors[field].as_text()

    form = CertificateForm()
    fields, page_obj, object_list = get_objects_and_pagination(request, Certificate, form)
    context = {
        'title': 'Certificates',
        'form': form,
        'errors': error,
        'message': message,
        'page_obj': page_obj,
        'fields': fields,
        'object_list': object_list,
        'model': 'Certificate'
    }
    return render(request, 'coffee/tables_example.html', context)


@login_required()
def table_order_page(request):
    error = {}
    message = ''
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            form.save()
            message = 'Added successful!'
            #return HttpResponseRedirect(reverse('coffee:form_owner'))
        else:
            for field in form.errors:
                error[field] = form.errors[field].as_text()

    form = OrderForm()
    fields, page_obj, object_list = get_objects_and_pagination(request, Order, form)

    context = {
        'title': 'Orders',
        'form': form,
        'errors': error,
        'message': message,
        'page_obj': page_obj,
        'fields': fields,
        'object_list': object_list,
        'model': 'Order'
    }
    return render(request, 'coffee/tables_example.html', context)


@login_required()
def table_payment_page(request):
    error = {}
    message = ''
    if request.method == 'POST':
        form = PaymentForm(request.POST)
        if form.is_valid():
            form.save()
            message = 'Added successful!'
            #return HttpResponseRedirect(reverse('coffee:form_owner'))
        else:
            for field in form.errors:
                error[field] = form.errors[field].as_text()

    form = PaymentForm()
    fields, page_obj, object_list = get_objects_and_pagination(request, Payment, form)

    context = {
        'title': 'Payments',
        'form': form,
        'errors': error,
        'message': message,
        'page_obj': page_obj,
        'fields': fields,
        'object_list': object_list,
        'model': 'Payment'
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
    paginator = Paginator(model_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    object_list = [obj.get_values() for obj in page_obj.object_list]
    return fields, page_obj, object_list


def delete_row(request):
    if request.method == 'DELETE':
        model = apps.get_model('coffee', QueryDict(request.body).get('model'))
        row = model.objects.get(pk=int(QueryDict(request.body).get('id')))
        row.delete()
        data = {
            'deleted': True,
        }
        return JsonResponse(data)

