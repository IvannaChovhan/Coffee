import django.forms as forms
import datetime

from crispy_forms.helper import FormHelper
from crispy_forms.layout import *
from django.forms import ModelForm

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
        labels = {
            "nameOwner": "Name",
            "phoneNumberOwner": "Phone number",
            "emailOwner": "E-mail"
        }
        error_messages={
            'null': 'null error',
            'required': 'required error'
        }

    def __init__(self, *args, **kwargs):
        super(OwnerForm, self).__init__(*args, **kwargs)
        self.fields['phoneNumberOwner'].required = True
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('nameOwner', css_class='form-group col-md-3 mb-0'),
                Column(Field("phoneNumberOwner", pattern="^\+?1?\d{9,15}$"), css_class='form-group col-md-3 mb-0'),
                Column('emailOwner', css_class='form-group col-md-3 mb-0'),
                Column(Submit('submit', '+ Add', css_class='btn btn-primary btn btn-succes mb-3 pr-4 pl-4'),
                       css_class="form-group col-md-3 mb-0 d-flex align-items-end"),
                css_class='form-row'
            ),

        )


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



