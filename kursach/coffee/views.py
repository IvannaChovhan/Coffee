from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate
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
    if request.method == 'POST':
        logout(request)
        return redirect('coffee:login')


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

    context = {
        'title': 'Countries',
        'form': form,
        'errors': error,
        'message': message,
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

    context = {
        'title': 'Coffee types',
        'form': form,
        'errors': error,
        'message': message,
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

    context = {
        'title': 'Buyers',
        'form': form,
        'errors': error,
        'message': message,
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

    context = {
        'title': 'Farm owners',
        'form': form,
        'errors': error,
        'message': message,
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

    context = {
        'title': 'Farms',
        'form': form,
        'errors': error,
        'message': message,
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

    context = {
        'title': 'Coffee products',
        'form': form,
        'errors': error,
        'message': message,
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

    context = {
        'title': 'Certificates',
        'form': form,
        'errors': error,
        'message': message,
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

    context = {
        'title': 'Orders',
        'form': form,
        'errors': error,
        'message': message,
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

    context = {
        'title': 'Payments',
        'form': form,
        'errors': error,
        'message': message,
    }
    return render(request, 'coffee/tables_example.html', context)

# @login_required()
# def form_owner(request):
#     error = {}
#     message = ''
#     title = 'Додати запис'
#     if request.method == 'POST':
#         form = OwnerForm(request.POST)
#         form.full_clean()
#         if form.is_valid():
#             form.save()
#             message = 'Запис успішно додано'
#             #return HttpResponseRedirect(reverse('coffee:form_owner'))
#         else:
#             for field in form.errors:
#                 error[field] = form.errors[field].as_text()
#
#     form = OwnerForm()
#
#     print(error)
#
#     context = {
#         'title': title,
#         'form': form,
#         'errors': form.errors,
#         'message': message,
#     }
#     return render(request, 'coffee/form.html', context)
