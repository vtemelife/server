from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class MailConfig(AppConfig):
    name = "apps.mail"
    verbose_name = _("Mail")
