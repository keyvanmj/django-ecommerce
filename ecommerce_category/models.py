from django.db import models
from django.urls import reverse

from ecommerce_manager.models import ProductManager, AbstractModel


class Category(AbstractModel):
    title = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100)
    is_active = models.BooleanField(default=True)
    description = models.TextField(default='all', blank=True)
    meta_keywords = models.CharField(
        'Meta Keywords', max_length=255, help_text='Comma-delimited set of SEO keywords for meta tag',
        default='ecommerce'
    )
    meta_description = models.CharField(
        'Meta Description', max_length=255, help_text='Content for description meta tag',
        default='we have everything you need'

    )
    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    parent = models.ForeignKey(
        'self', on_delete=models.SET_NULL, blank=True, null=True, related_name='children', default=None
    )
    objects = ProductManager()

    class Meta(AbstractModel.Meta):
        verbose_name_plural = 'Categories'
        ordering = ['parent__id', '-created_at']
        unique_together = ('slug', 'parent')

    def __str__(self):
        full_path = [self.title]
        k = self.parent
        while k is not None:
            full_path.append(k.title)
            k = k.parent
        return ' --> '.join(full_path[::-1])

    def get_absolute_url(self):
        return reverse('category_view', kwargs={'hierarchy': self.slug})

    def get_cat_list(self):
        k = self
        breadcrumb = ['dummy']
        while k is not None:
            breadcrumb.append(k.title)
            k = k.parent
        for i in range(len(breadcrumb)-3):
            breadcrumb[i] = '/'.join(breadcrumb)
        return breadcrumb[-1:0:-1]
