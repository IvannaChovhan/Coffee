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
        labels = {
            "nameCountry": "Name of country",
        }

    def __init__(self, *args, **kwargs):
        super(CountryForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('nameCountry', css_class='form-group col-md-3 mb-0'),
                Column(Submit('submit', '+ Add', css_class='btn btn-primary btn btn-succes mb-3 pr-4 pl-4'),
                       css_class="form-group col-md-3 mb-0 d-flex align-items-end"),
                css_class='form-row'
            ),

        )


class CoffeeTypeForm(ModelForm):
    class Meta:
        model = CoffeeType
        fields = ['nameCoffeeType']
        labels = {
            "nameCoffeeType": "Name of coffee type",
        }

    def __init__(self, *args, **kwargs):
        super(CoffeeTypeForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('nameCoffeeType', css_class='form-group col-md-3 mb-0'),
                Column(Submit('submit', '+ Add', css_class='btn btn-primary btn btn-succes mb-3 pr-4 pl-4'),
                       css_class="form-group col-md-3 mb-0 d-flex align-items-end"),
                css_class='form-row'
            ),

        )


class BuyerForm(ModelForm):
    class Meta:
        model = Buyer
        fields = ['nameBuyer', 'phoneNumberBuyer', 'emailBuyer']
        labels = {
            "nameBuyer": "Name",
            "phoneNumberBuyer": "Phone number",
            "emailBuyer": "E-mail"
        }

    def __init__(self, *args, **kwargs):
        super(OwnerForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('nameBuyer', css_class='form-group col-md-3 mb-0'),
                Column(Field("phoneNumberBuyer", pattern="^\+?1?\d{9,15}$"), css_class='form-group col-md-3 mb-0'),
                Column('emailBuyer', css_class='form-group col-md-3 mb-0'),
                Column(Submit('submit', '+ Add', css_class='btn btn-primary btn btn-succes mb-3 pr-4 pl-4'),
                       css_class="form-group col-md-3 mb-0 d-flex align-items-end"),
                css_class='form-row'
            ),

        )


class OwnerForm(ModelForm):
    class Meta:
        model = Owner
        fields = ['nameOwner', 'phoneNumberOwner', 'emailOwner']
        labels = {
            "nameOwner": "Name",
            "phoneNumberOwner": "Phone number",
            "emailOwner": "E-mail"
        }

    def __init__(self, *args, **kwargs):
        super(OwnerForm, self).__init__(*args, **kwargs)
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
        labels = {
            "nameFarm": "Name",
            "ownerFarm": "Owner",
            "countryFarm": "Country"
        }

    def __init__(self, *args, **kwargs):
        super(FarmForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('nameFarm', css_class='form-group col-md-3 mb-0'),
                Column('ownerFarm', css_class='form-group col-md-3 mb-0'),
                Column('countryFarm', css_class='form-group col-md-3 mb-0'),
                Column(Submit('submit', '+ Add', css_class='btn btn-primary btn btn-succes mb-3 pr-4 pl-4'),
                       css_class="form-group col-md-3 mb-0 d-flex align-items-end"),
                css_class='form-row'
            ),

        )


class CoffeeProductForm(ModelForm):
    class Meta:
        model = CoffeeProduct
        fields = ['coffeeType', 'harvestYear',
                  'farm', 'aroma', 'aftertaste', 'flavor', 'color']
        labels = {
            "coffeeType": "Type of coffee",
            "harvestYear": "Harvest year",
            "farm": "Farm",
            "aroma": "Aroma",
            "aftertaste": "Aftertaste",
            "flavor": "Flavor",
            "color": "Color"
        }

    def __init__(self, *args, **kwargs):
        super(CoffeeProductForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('coffeeType', css_class='form-group col-md-2 mb-0'),
                Column('harvestYear', css_class='form-group col-md-1 mb-0'),
                Column('farm', css_class='form-group col-md-3 mb-0'),
                Column('aroma', css_class='form-group col-md-1 mb-0'),
                Column('aftertaste', css_class='form-group col-md-1 mb-0'),
                Column('flavor', css_class='form-group col-md-1 mb-0'),
                Column('color', css_class='form-group col-md-1 mb-0'),
                Column(Submit('submit', '+ Add', css_class='btn btn-primary btn btn-succes mb-3 pr-4 pl-4'),
                       css_class="form-group col-md-1 mb-0 d-flex align-items-end"),
                css_class='form-row'
            ),

        )


class CertificateForm(ModelForm):
    class Meta:
        model = Certificate
        fields = ['body', 'product', 'dateOfExpire', 'disadvantages']
        labels = {
            "body": "Text of certificate",
            "product": "For product",
            "dateOfExpire": "Date of expire",
            "disadvantages": "Disadvantages",
        }

    def __init__(self, *args, **kwargs):
        super(CertificateForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('body', css_class='form-group text-area-form col-md-3 mb-0'),
                Column('disadvantages', css_class='form-group text-area-form col-md-3 mb-0'),
                Column('product', css_class='form-group col-md-1 mb-0'),
                Column('dateOfExpire', css_class='form-group col-md-2 mb-0'),
                Column(Submit('submit', '+ Add', css_class='btn btn-primary btn btn-succes margin-30 pr-4 pl-4'),
                       css_class="form-group col-md-1 mb-0 d-flex align-items-start"),
                css_class='form-row'
            ),

        )


class OrderForm(ModelForm):
    class Meta:
        model = Order
        fields = ['coffeeProduct', 'weight', 'price', 'dateOrder', 'buyer', 'purchase']
        labels = {
            "coffeeProduct": "Coffee product",
            "weight": "Weight, kg",
            "price": "Price, $",
            "dateOrder": "Date of order",
            "buyer": "Buyer",
            "purchase": "Purchase",
        }

    def __init__(self, *args, **kwargs):
        super(OrderForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('coffeeProduct', css_class='form-group col-md-2 mb-0'),
                Column('weight', css_class='form-group col-md-1 mb-0'),
                Column('price', css_class='form-group col-md-1 mb-0'),
                Column('dateOrder', css_class='form-group col-md-2 mb-0'),
                Column('buyer', css_class='form-group col-md-3 mb-0'),
                Column('purchase', css_class='form-group col-md-1 mb-0'),
                Column(Submit('submit', '+ Add', css_class='btn btn-primary btn btn-succes mb-3 pr-4 pl-4'),
                       css_class="form-group col-md-1 mb-0 d-flex align-items-end"),
                css_class='form-row'
            ),

        )


class PaymentForm(ModelForm):
    class Meta:
        model = Payment
        fields = ['order', 'datePayment', 'amount']
        labels = {
            "order": "Number of order",
            "datePayment": "Date of payment",
            "amount": "Amount, $"
        }

    def __init__(self, *args, **kwargs):
        super(PaymentForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('order', css_class='form-group col-md-2 mb-0'),
                Column('datePayment', css_class='form-group col-md-2 mb-0'),
                Column('amount', css_class='form-group col-md-1 mb-0'),
                Column(Submit('submit', '+ Add', css_class='btn btn-primary btn btn-succes mb-3 pr-4 pl-4'),
                       css_class="form-group col-md-3 mb-0 d-flex align-items-end"),
                css_class='form-row'
            ),

        )



