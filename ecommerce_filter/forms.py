from django import forms

from ecommerce.models import Product
from ecommerce_category.models import Category


class CategoryProductFilter(forms.Form):
    all = forms.BooleanField(label='همه ی دسته بندی ها', required=False,
                             widget=forms.CheckboxInput(attrs={'value': 'همه'}))

    def __init__(self, *args, **kwargs):
        super(CategoryProductFilter, self).__init__(*args, **kwargs)
        categories = Category.objects.all()
        for i in categories:
            if i.parent == None:
                self.fields[f'{i.slug}'] = forms.BooleanField(
                    required=False, label=f'{i}',
                    widget=forms.CheckboxInput(attrs={'value': i, 'name': i.title, 'class': 'updating'}))
