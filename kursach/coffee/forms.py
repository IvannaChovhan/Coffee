import django.forms as forms
import datetime
from .models import *


class CountryForm(ModelForm):
    class Meta:
        model = Country
        fields = ['nameCountry']


class CoffeeTypeForm(ModelForm):
    class Meta:
        model = CoffeeType
        fields = ['nameCoffeeType']


class BuyerForm(ModelForm):
    class Meta:
        model = Buyer
        fields = ['nameBuyer', 'phoneNumberBuyer', 'emailBuyer']


class OwnerForm(ModelForm):
    class Meta:
        model = Owner
        fields = ['nameOwner', 'phoneNumberOwner', 'emailOwner']


class FarmForm(ModelForm):
    class Meta:
        model = Farm
        fields = ['nameFarm', 'ownerFarm', 'countryFarm']


class CoffeeProductForm(ModelForm):
    class Meta:
        model = CoffeeProduct
        fields = ['coffeeType', 'harvestYear',
                  'farm', 'aroma', 'aftertaste', 'flavor', 'color']


class CertificateForm(ModelForm):
    class Meta:
        model = Certificate
        fields = ['body', 'product', 'dateOfExpire', 'disadvantages']


class OrderForm(ModelForm):
    class Meta:
        model = Order
        fields = ['coffeeProduct', 'weight', 'price', 'dateOrder', 'buyer', 'purchase']


class PaymentForm(ModelForm):
    class Meta:
        model = Payment
        fields = ['order', 'datePayment', 'amount']
