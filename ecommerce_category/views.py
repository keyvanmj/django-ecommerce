from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView
from ecommerce_filter.forms import CategoryProductFilter
from Django_ECommerce import settings
from ecommerce.models import Product
from ecommerce_category.models import Category


def ecomstore(request):
    return {
        'active_categories': Category.objects.filter(is_active=True),
        'site_name': settings.SITE_NAME,
        'meta_keywords': settings.META_KEYWORDS,
        'meta_description': settings.META_DESCRIPTION,
        'request': request
    }


class CategoryView(ListView):
    template_name = 'products/product_list.html'
    paginate_by = 8

    def get_queryset(self):
        return Product.objects.get_by_category(slug=self.kwargs['hierarchy'])



    def get_context_data(self, **kwargs):
        hierarchy = self.kwargs['hierarchy']
        category = get_object_or_404(Category, slug=hierarchy)
        context = super(CategoryView, self).get_context_data(**kwargs)

        context['subcategories']: category.children.all()
        context['category'] = Category.objects.all()
        context['form'] = CategoryProductFilter
        context['slg'] = hierarchy
        context['cat_list'] = category.get_cat_list()
        return context
