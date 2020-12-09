from django.shortcuts import render

# Create your views here.
from django.urls import reverse
from .forms import *


def get_all_fields_from_form(instance):
    """"
    Return names of all available fields from given Form instance.

    :arg instance: Form instance
    :returns list of field names
    :rtype: list
    """

    fields = list(instance().base_fields)

    for field in list(instance().declared_fields):
        if field not in fields:
            fields.append(field)
    return fields


def index(request):
    return render(request, 'coffee/index.html')


def table_countries_page(request):
    context = {
        'title': 'Країни',
    }
    return render(request, 'coffee/tables_example.html', context)


def table_owner_page(request):
    context = {
        'title': 'Власник',
        'link_to_add_row': reverse('coffee: form_owner')
    }
    return render(request, 'coffee/tables_example.html', context)


def form_owner(request):
    error = ''
    title = 'Додати запис'
    if request.method == 'POST':
        form = OwnerForm(request.POST)
        if form.is_valid():
            form.save()
        else:
            error = "Сталася помилка"

    form = OwnerForm()
    fields = get_all_fields_from_form(form)
    context = {
        'title': title,
        'form': form,
        'error': error,
        'fields': fields
    }
    return render(request, 'coffee/form.html', context)
