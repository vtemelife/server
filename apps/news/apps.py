from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class NewsConfig(AppConfig):
    name = "apps.news"
    verbose_name = _("News")

    def ready(self):
        import apps.news.signals  # noqa
