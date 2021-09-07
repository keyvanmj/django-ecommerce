from datetime import datetime, timedelta

from django.db import models
from django.db.models import Q, Count

class ProductQueryset(models.query.QuerySet):
    def filter_products(self, request):
        action = request.GET.get('action')
        if action == 'last':
            return self.filter(active=True).order_by('-created')
        elif action == 'cheap':
            return self.filter(active=True).order_by('price')
        elif action == 'expensive':
            return self.filter(active=True).order_by('-price')
        elif action == 'most_view':
            last_month = datetime.today() - timedelta(days=30)
            return self.filter(active=True).annotate(count=Count(
                'hits', filter=Q(producthit__created__gte=last_month))).order_by('-count', '-created')

        elif action == 'favourites':
            return self.filter(active=True).annotate(count=Count(
                'hits' and 'favourite')).order_by('-count', '-created')
        elif action == 'most_sells':
            return self.filter(active=True).annotate(count=Count(
                'cartproduct__cart__order')).order_by('-count')



class ProductManager(models.Manager):
    def get_queryset(self):
        return ProductQueryset(self.model,using=self._db)

    def get_active_products(self):
        return self.get_queryset().filter(active=True)

    def get_product_id(self, pk):
        qs = self.get_queryset().filter(id=pk)
        if qs.count() == 1:
            return qs.first()
        return None


    def get_by_category(self,slug):
        product_category = (
                Q(category__slug__iexact=slug) |
                Q(category__parent__slug__iexact=slug) |
                Q(category__parent__parent__slug__iexact=slug)
        )
        return self.get_queryset().filter(product_category).distinct()


    def most_sell_products(self):
        return self.get_queryset().filter(active=True).annotate(count=Count(
            'cartproduct__cart__order')).order_by('-count')[:5]


class FeaturedProductManager(models.Manager):
    def all(self):
        return super(FeaturedProductManager, self).all().filter(active=True)


class AbstractModel(models.Model):
    class Meta:
        abstract = True

    objects = ProductManager()

