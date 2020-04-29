from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class CommentsConfig(AppConfig):
    name = "apps.comments"
    verbose_name = _("Comments")
