from apps.generic.models import GenericModelMixin
from ckeditor_uploader.fields import RichTextUploadingField
from django.db import models
from django.utils.translation import ugettext_lazy as _


class MobileVersion(GenericModelMixin, models.Model):
    version = models.CharField(_("Version"), max_length=255)
    android_apk = models.FileField(verbose_name=_("Android APK"), null=True, blank=True)

    readme = RichTextUploadingField(_("Readme"), config_name="basic", null=True, blank=False)

    class Meta:
        verbose_name = _("Mobile Version")
        verbose_name_plural = _("Mobile Versions")
        ordering = ["-created_date"]
