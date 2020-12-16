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
import csv, io


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
            #return HttpResponseRedirect(reverse('coffee:form_owner'))
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
            #return HttpResponseRedirect(reverse('coffee:form_owner'))
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
            #return HttpResponseRedirect(reverse('coffee:form_owner'))
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
            #return HttpResponseRedirect(reverse('coffee:form_owner'))
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
            #return HttpResponseRedirect(reverse('coffee:form_owner'))
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
    paginator = Paginator(model_list, 50)
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
