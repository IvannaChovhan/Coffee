import django.forms as forms
import datetime

from kursach.coffee.models import current_year


def year_choices():
    return [(r, r) for r in range(1984, datetime.date.today().year + 1)]


class MyForm(forms.ModelForm):
    year = forms.TypedChoiceField(coerce=int, choices=year_choices, initial=current_year)
