from django.apps import AppConfig


class EcommerceProfileConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'ecommerce_profile'

    def ready(self):
        import ecommerce_profile.signals