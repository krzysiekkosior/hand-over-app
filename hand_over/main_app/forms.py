from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


def validate_unique_username(value):
    if User.objects.filter(username=value).count() != 0:
        raise ValidationError("Podany email jest zajęty.")


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


# first_name = forms.CharField(max_length=30, widget=forms.TextInput(attrs={'placeholder': 'Imię'}))
# last_name = forms.CharField(max_length=30, widget=forms.TextInput(attrs={'placeholder': 'Nazwisko'}))
# email = forms.EmailField(max_length=254, widget=forms.TextInput(attrs={'placeholder': 'Email'}))
