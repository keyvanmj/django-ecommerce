from django import forms
from .models import SearchTerm


class SearchForm(forms.ModelForm):
    class Meta:
        model = SearchTerm
        fields = ['q']

    def __init__(self,*args,**kwargs):
        super(SearchForm, self).__init__(*args,**kwargs)
        self.fields['q'].widget.attrs['placeholder'] = 'جستجو'
        for field_name,field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.widget.attrs['class'] = 'search_class'

    include = ('q',)