from apps.generic.models import GenericModelMixin
from django.db import models
from django.utils.translation import ugettext_lazy as _


class Email(GenericModelMixin, models.Model):
    from_email = models.CharField(_("From email"), max_length=255)
    to_emails = models.TextField(_("To emails"))

    subject = models.CharField(_("Subject"), max_length=255)
    body = models.TextField(_("Body"))

    class Meta:
        verbose_name = _("Email")
        verbose_name_plural = _("Emails")
        ordering = ["-created_date"]
