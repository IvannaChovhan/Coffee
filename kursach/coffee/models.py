from django.db import models
from django.core.validators import RegexValidator, MaxValueValidator, MinValueValidator

import datetime


def current_year():
    return datetime.date.today().year


def max_value_current_year():
    return MaxValueValidator(current_year())


def year_choices():
    return ((r, r) for r in range(1984, current_year() + 1))


BUY_SELL_CHOICES = (
    ('BUY', 'Закупка'),
    ('SELL', 'Продаж')
)


def get_phone_regex():
    return RegexValidator(regex=r'^\+?1?\d{9,15}$',
                          message="Phone number must be in format: '+999999999'. Up to 15 digits allowed")


# Create your models here.
class CoffeeType(models.Model):
    nameCoffeeType = models.CharField(max_length=50,
                                      error_messages={"invalid": "Name is too long. Up to 50 symbols allowed",
                                                      "required": "Name field is required"})

    def __str__(self):
        return u'{0}'.format(self.nameCoffeeType)

    def get_values(self):
        return [self.id, self.nameCoffeeType]


class Buyer(models.Model):
    nameBuyer = models.CharField(max_length=50, error_messages={"invalid": "Name is too long. Up to 50 symbols allowed",
                                                                "required": "Name field is required"})
    # https://stackoverflow.com/questions/19130942/whats-the-best-way-to-store-phone-number-in-django-models
    phoneNumberBuyer = models.CharField(validators=[get_phone_regex()], max_length=17,
                                        error_messages={
                                            "required": "Phone number is required"})  # validators should be a list
    emailBuyer = models.EmailField(error_messages={"invalid": "E-mail field is incorrect", "required": "E-mail field "
                                                                                                       "is required"})

    def __str__(self):
        return u'{0}'.format(self.nameBuyer)

    def get_values(self):
        return [self.id, self.nameBuyer, self.phoneNumberBuyer, self.emailBuyer]


class Owner(models.Model):
    nameOwner = models.CharField(max_length=50, error_messages={"invalid": "Name is too long. Up to 50 symbols allowed",
                                                                "required": "Name field is required"})
    phoneNumberOwner = models.CharField(validators=[get_phone_regex()], max_length=17,
                                        error_messages={
                                            "required": "Phone number is required"})  # validators should be a list
    emailOwner = models.EmailField(error_messages={"invalid": "E-mail field is incorrect", "required": "E-mail field "
                                                                                                       "is required"})

    def __str__(self):
        return u'{0}'.format(self.nameOwner)

    def get_values(self):
        return [self.id, self.nameOwner, self.phoneNumberOwner, self.emailOwner]


class Country(models.Model):
    nameCountry = models.CharField(max_length=50,
                                   error_messages={"invalid": "Name is too long. Up to 50 symbols allowed",
                                                   "required": "Name field is required"})

    def __str__(self):
        return u'{0}'.format(self.nameCountry)

    def get_values(self):
        return [self.id, self.nameCountry]


class Farm(models.Model):
    nameFarm = models.CharField(max_length=40, error_messages={"invalid": "Name is too long. Up to 50 symbols allowed",
                                                               "required": "Name field is required"})
    ownerFarm = models.ForeignKey(Owner, models.CASCADE)
    countryFarm = models.ForeignKey(Country, models.CASCADE)

    def __str__(self):
        return u'{0} ({1})'.format(self.nameFarm, self.countryFarm)

    def get_values(self):
        return [self.id, self.nameFarm, self.ownerFarm, self.countryFarm]


class CoffeeProduct(models.Model):
    coffeeType = models.ForeignKey(CoffeeType, on_delete=models.CASCADE)
    # https://stackoverflow.com/questions/49051017/year-field-in-django
    harvestYear = models.IntegerField(choices=year_choices(), default=current_year(),
                                      validators=[MinValueValidator(1984), max_value_current_year()],
                                      error_messages={
                                          "invalid": "Harvest year must be from 1984 to {}".format(current_year()),
                                          "required": "Harvest year is required"})
    farm = models.ForeignKey(Farm, models.CASCADE)
    aroma = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(10)],
                              error_messages={"invalid": "Aroma field must be from 0 to 10",
                                              "required": "Aroma field is required"}
                              )
    aftertaste = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(10)],
                                   error_messages={"invalid": "Aftertaste field must be from 0 to 10",
                                                   "required": "Aftertaste field is required"}
                                   )
    flavor = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(10)],
                               error_messages={"invalid": "Flavor field must be from 0 to 10",
                                               "required": "Flavor field is required"}
                               )
    color = models.CharField(max_length=20, error_messages={"invalid": "Color is too long. Up to 20 symbols allowed",
                                                            "required": "Color field is required"})

    def __str__(self):
        return u'{0}'.format(self.id)

    def get_values(self):
        return [self.id, self.coffeeType, self.harvestYear, self.farm, self.aroma, self.aftertaste, self.flavor, self.color]


class Certificate(models.Model):
    body = models.TextField(max_length=500, error_messages={"invalid": "Text of certificate is too long. "
                                                                       "Up to 500 symbols allowed",
                                                            "required": "Text of certificate is required"})
    product = models.OneToOneField(CoffeeProduct, models.CASCADE)
    dateOfExpire = models.DateField(error_messages={"required": "Date of expire is required"})
    disadvantages = models.TextField(max_length=500, error_messages={"invalid": "Disadvantages field is too long. "
                                                                                "Up to 500 symbols allowed",
                                                                     "required": "Disadvantages field is required"})

    def get_values(self):
        return [self.id, self.body, self.product, self.dateOfExpire, self.disadvantages]


class Order(models.Model):
    coffeeProduct = models.ForeignKey(CoffeeProduct, models.CASCADE)
    weight = models.FloatField(validators=[MinValueValidator(0)],
                               error_messages={"invalid": "Weight field must be positive float",
                                               "required": "Weight is required"})
    price = models.DecimalField(decimal_places=2, max_digits=20, validators=[MinValueValidator(0)],
                                error_messages={
                                    "invalid": "Price field must be positive float. Up to 20 digits allowed",
                                    "required": "Price is required"}
                                )
    dateOrder = models.DateField()
    buyer = models.ForeignKey(Buyer, models.CASCADE)
    purchase = models.CharField(max_length=4,
                                choices=BUY_SELL_CHOICES,
                                default='BUY')

    def __str__(self):
        return u'{0}'.format(self.id)

    def get_values(self):
        return [self.id, self.coffeeProduct, self.weight, self.price, self.dateOrder, self.buyer, self.purchase]


class Payment(models.Model):
    order = models.ForeignKey(Order, models.CASCADE)
    datePayment = models.DateField(error_messages={"required": "Date is required"})
    amount = models.DecimalField(decimal_places=2, max_digits=20, validators=[MinValueValidator(0)],
                                 error_messages={
                                     "invalid": "Amount field must be positive float. Up to 20 digits allowed",
                                     "required": "Amount is required"})

    def get_values(self):
        return [self.id, self.order, self.datePayment, self.amount]
