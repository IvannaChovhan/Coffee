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
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
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
    context = {
        'title': 'Країни',
    }
    return render(request, 'coffee/tables_example.html', context)


@login_required()
def table_owner_page(request):
    context = {
        'title': 'Власник',
        'link_to_add_row': reverse('coffee:form_owner')
    }
    return render(request, 'coffee/tables_example.html', context)


@login_required()
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
