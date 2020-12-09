from django.shortcuts import render

# Create your views here.
from django.urls import reverse
from .forms import *


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
        'link_to_add_row': reverse('coffee:form_owner')
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

    context = {
        'title': title,
        'form': form,
        'error': error,
    }
    return render(request, 'coffee/form.html', context)
