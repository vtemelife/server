from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class ClubsConfig(AppConfig):
    name = "apps.clubs"
    verbose_name = _("Clubs")

    def ready(self):
        import apps.clubs.signals  # noqa
