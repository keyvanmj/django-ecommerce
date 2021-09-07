from django import forms
from .models import Category
class CategoryFilterForm(forms.Form):
    checkbox_category = forms.BooleanField(label='')