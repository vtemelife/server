from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class GamesConfig(AppConfig):
    name = "apps.games"
    verbose_name = _("Games")

    def ready(self):
        import apps.games.signals  # noqa
