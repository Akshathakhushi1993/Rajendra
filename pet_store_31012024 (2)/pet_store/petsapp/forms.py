from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import ShippingAddress, Customer

PRODUCT_QUANTITY_CHOICES = [(i, str(i)) for i in range(1, 21)]


class UserCustomRegisterForm(UserCreationForm):
    first_name = forms.CharField(max_length=50)
    last_name = forms.CharField(max_length=50)
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']


class UserCustomRegisterForm2(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['phone']


class SearchForm(forms.Form):
    q = forms.CharField(label='search', max_length=50)


class CartAddProductForm(forms.Form):
    quantity = forms.TypedChoiceField(choices=PRODUCT_QUANTITY_CHOICES, coerce=int)
    update = forms.BooleanField(required=False, initial=False, widget=forms.HiddenInput)


class ShippingAddressForm(forms.ModelForm):
    class Meta:
        model = ShippingAddress
        fields = ['building_name', 'street', 'landmark', 'city', 'state', 'zipcode']


class SetDeliveryAddressForm(forms.Form):
    delivery_address = forms.CharField()
