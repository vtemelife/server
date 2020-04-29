from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class MembershipsConfig(AppConfig):
    name = "apps.memberships"
    verbose_name = _("Memberships")

    def ready(self):
        import apps.memberships.signals  # noqa
