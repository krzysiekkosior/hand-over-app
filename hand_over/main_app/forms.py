import re
from datetime import datetime

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from main_app.models import Donation, Category, Institution


def validate_unique_username(value):
    if User.objects.filter(username=value).count() != 0:
        raise ValidationError("Podany email jest zajęty.")


def validate_zip_code(value):
    validator = r'^[0-9]{2}-[0-9]{3}$'
    if re.search(validator, value) is None:
        raise ValidationError("Podaj poprawny kod pocztowy")


def validate_date(value):
    today = datetime.today().date()
    if value < today:
        raise ValidationError("Data nie może być z przeszłości")

class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'password1', 'password2',)

    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].required = True
        self.fields['first_name'].widget.attrs['placeholder'] = 'Imię'
        self.fields['last_name'].required = True
        self.fields['last_name'].widget.attrs['placeholder'] = 'Nazwisko'
        self.fields['password1'].widget.attrs['placeholder'] = 'Hasło'
        self.fields['password2'].widget.attrs['placeholder'] = 'Powtórz hasło'
        self.fields['email'].widget.attrs['placeholder'] = 'Email'
        self.fields['email'].required = True
        self.fields['email'].validators.append(validate_unique_username)


class DonationForm(forms.ModelForm):
    categories = forms.ModelMultipleChoiceField(queryset=Category.objects.all())
    institution = forms.ModelChoiceField(queryset=Institution.objects.all())

    class Meta:
        model = Donation
        exclude = ('user', )
        error_messages = {
            'address': {'required': 'Podaj adres dostawy'},
            'quantity': {'required': 'Podaj liczbę worków',
                         'min_value': 'Podaj liczbę worków'},
            'phone_number': {'required': 'Podaj numer kontaktowy'},
            'city': {'required': 'Podaj miasto'},
            'zip_code': {'required': 'Podaj kod pocztowy'},
            'pick_up_date': {'required': 'Podaj datę odbioru'},
            'pick_up_time': {'required': 'Podaj godzinę odbioru'}
        }

