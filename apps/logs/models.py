import logging

from django.db import models
from django.utils.translation import ugettext_lazy as _

from apps.generic.models import GenericModelMixin


class Log(GenericModelMixin, models.Model):
    LOG_LEVELS = (
        (logging.NOTSET, _("NotSet")),
        (logging.INFO, _("Info")),
        (logging.WARNING, _("Warning")),
        (logging.DEBUG, _("Debug")),
        (logging.ERROR, _("Error")),
        (logging.FATAL, _("Fatal")),
    )

    logger_name = models.CharField(_("Logger name"), max_length=100)
    level = models.PositiveSmallIntegerField(_("Level"), choices=LOG_LEVELS, default=logging.ERROR, db_index=True)
    msg = models.TextField(_("Msg"))
    trace = models.TextField(_("Trace"), blank=True, null=True)

    def __str__(self):
        return self.msg

    class Meta:
        ordering = ("-created_date",)
        verbose_name_plural = _("Logs")
        verbose_name = _("Log")
