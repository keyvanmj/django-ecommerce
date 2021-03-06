from django.apps import AppConfig


class EcommerceCartConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'ecommerce_cart'

    def ready(self):
        import ecommerce_cart.signals
