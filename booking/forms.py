from django.forms import ModelForm, TextInput
from .models import Ticket
from django import forms
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import authenticate, login
from django.shortcuts import redirect


class ticketForm(ModelForm):
    class Meta:
        model = Ticket
        fields = '__all__'
        labels = {
            'name': '',
            'origin': ('from'),
            'phone_no': '',
            'date_of_departure': '',
            'seat_no': '',
            'price': ''
        }
        # widgets to change or define attributes of form fields
        widgets = {
            'seat_no': TextInput(attrs={'readonly': 'readonly', 'placeholder': 'Select the seat number'}),
            'price': TextInput(attrs={'readonly': 'readonly', 'placeholder': 'Price for the trip'}),
            'name': TextInput(attrs={'placeholder': 'Name'}),

            'phone_no': TextInput(attrs={'placeholder': 'Phone number', "size":"10"}),
            'date_of_departure': TextInput(attrs={'placeholder': 'Date of depature'}),
        }
        help_texts = {
            'seat_no': _('please select a seat on your right'),
        }


class adminLoginForm(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(max_length=100, widget=forms.PasswordInput)

    def clean(self):
        # Get login data
        username = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")

        if username and password:
            user = authenticate(username=username, password=password)
            if user is not None:
                return self.cleaned_data
            else:
                raise forms.ValidationError(
                    "You have entered a wrong email or password")


class routesForm(forms.Form):
    NAIROBI = 'NRB'
    NAKURU = 'NKR'
    ELDORET = 'ELD'
    KISUMU = 'KSM'
    KAKAMEGA = 'KMG'
    BUNGOMA = 'BNM'

    cities = (
        (NAIROBI, 'Nairobi'),
        (NAKURU, 'Nakuru'),
        (KAKAMEGA, 'Kakamega'),
        (ELDORET, 'Eldoret'),
        (KISUMU, 'Kisumu'),
        (BUNGOMA, 'Bungoma'),
    )

    to = forms.ChoiceField(choices=cities,required=True)
    origin = forms.ChoiceField(choices=cities,required=True)
