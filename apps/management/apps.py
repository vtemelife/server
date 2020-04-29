from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class ManagementConfig(AppConfig):
    name = "apps.management"
    verbose_name = _("Management")

    def ready(self):
        import apps.management.signals  # noqa
