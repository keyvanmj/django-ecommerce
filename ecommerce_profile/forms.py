from django import forms
from django.utils.translation import ugettext_lazy as _
from accounts.forms import phone_valid
from ecommerce_profile.models import Profile

class ProfileForm(forms.ModelForm):
    phone_number = forms.CharField(label=_('تلفن همراه'),widget=forms.NumberInput,validators=[phone_valid])
    class Meta:
        model = Profile
        fields = ['image']