from django.db import models
from django.core.validators import RegexValidator, MaxValueValidator, MinValueValidator
from django.forms import ModelForm
import datetime


def current_year():
    return datetime.date.today().year


def max_value_current_year():
    return MaxValueValidator(current_year())


def year_choices():
    return ((r, r) for r in range(1984, current_year()+1))


BUY_SELL_CHOICES = (
    ('BUY', 'Закупка'),
    ('SELL', 'Продаж')
)


def get_phone_regex():
    return RegexValidator(regex=r'^\+?1?\d{9,15}$',
                          message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")


# Create your models here.
class CoffeeType(models.Model):
    nameCoffeeType = models.CharField(max_length=50)


class Buyer(models.Model):
    nameBuyer = models.CharField(max_length=50)
    #https://stackoverflow.com/questions/19130942/whats-the-best-way-to-store-phone-number-in-django-models
    phoneNumberBuyer = models.CharField(validators=[get_phone_regex()], max_length=17, blank=True)  # validators should be a list
    emailBuyer = models.EmailField()


class Owner(models.Model):
    nameOwner = models.CharField(max_length=50)
    phoneNumberOwner = models.CharField(validators=[get_phone_regex()], max_length=17, blank=True)  # validators should be a list
    emailOwner = models.EmailField()


class Country(models.Model):
    nameCountry = models.CharField(max_length=50)


class Farm(models.Model):
    nameFarm = models.CharField(max_length=40)
    ownerFarm = models.ForeignKey(Owner, models.CASCADE)
    countryFarm = models.ForeignKey(Country, models.CASCADE)


class CoffeeProduct(models.Model):
    coffeeType = models.ForeignKey(CoffeeType, on_delete=models.CASCADE)
    #https://stackoverflow.com/questions/49051017/year-field-in-django
    harvestYear = models.IntegerField(choices=year_choices(), default=current_year(),
                                      validators=[MinValueValidator(1984), max_value_current_year()])
    farm = models.ForeignKey(Farm, models.CASCADE)
    aroma = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(10)])
    aftertaste = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(10)])
    flavor = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(10)])
    color = models.CharField(max_length=20)


class Certificate(models.Model):
    body = models.TextField(max_length=500)
    product = models.OneToOneField(CoffeeProduct, models.CASCADE)
    dateOfExpire = models.DateField()
    disadvantages = models.TextField(max_length=500)


class Order(models.Model):
    coffeeProduct = models.ForeignKey(CoffeeProduct, models.CASCADE)
    weight = models.FloatField(validators=[MinValueValidator(0)])
    price = models.DecimalField(decimal_places=2, max_digits=20, validators=[MinValueValidator(0)])
    dateOrder = models.DateField()
    buyer = models.ForeignKey(Buyer, models.CASCADE)
    purchase = models.CharField(max_length=4,
                                choices=BUY_SELL_CHOICES,
                                default='BUY')


class Payment(models.Model):
    order = models.ForeignKey(Order, models.CASCADE)
    datePayment = models.DateField()
    amount = models.DecimalField(decimal_places=2, max_digits=20, validators=[MinValueValidator(0)])


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
        fields = ['coffeeType', #'harvestYear',
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

