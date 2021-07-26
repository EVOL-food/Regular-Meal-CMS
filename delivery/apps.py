from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class DeliveryConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'delivery'
    verbose_name = _('Delivery')

    def ready(self):
        import delivery.signals
