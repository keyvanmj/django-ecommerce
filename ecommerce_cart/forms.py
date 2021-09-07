from django import forms
from .models import *


class CheckoutForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['full_name', 'mobile', 'email', 'shipping_address']
