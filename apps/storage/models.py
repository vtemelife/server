import logging

from apps.generic.models import GenericModelMixin
from django.db import models
from django.utils.translation import gettext_lazy as _
from imagekit.models import ImageSpecField
from imagekit.processors import SmartResize
from PIL import ImageFilter

logger = logging.getLogger("django")


class File(GenericModelMixin, models.Model):
    creator = models.ForeignKey(
        "users.User", verbose_name=_("Creator"), on_delete=models.CASCADE, blank=True, null=True
    )
    name = models.CharField(verbose_name=_("Name"), max_length=255, blank=True, null=True)
    file = models.FileField(verbose_name=_("File"))

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("File")
        verbose_name_plural = _("Files")


class BlurImage:
    def __init__(self, radius=10):
        self.radius = radius

    def process(self, img):
        return img.filter(ImageFilter.GaussianBlur(radius=self.radius))


class Image(GenericModelMixin, models.Model):
    creator = models.ForeignKey(
        "users.User", verbose_name=_("Creator"), on_delete=models.CASCADE, blank=True, null=True
    )
    name = models.CharField(verbose_name=_("Name"), max_length=255, blank=True, null=True)
    image = models.ImageField(verbose_name=_("Image"))

    thumbnail_100x100 = ImageSpecField(
        source="image",
        # processors=[ResizeToFit(200)],
        processors=[SmartResize(100, 100)],
        format="JPEG",
        options={"quality": 100},
    )

    thumbnail_500x500 = ImageSpecField(
        source="image", processors=[SmartResize(500, 500)], format="JPEG", options={"quality": 100}
    )

    thumbnail_blur_100x100 = ImageSpecField(
        source="image",
        # processors=[ResizeToFit(200)],
        processors=[SmartResize(100, 100), BlurImage()],
        format="JPEG",
        options={"quality": 100},
    )

    thumbnail_blur_500x500 = ImageSpecField(
        source="image", processors=[SmartResize(500, 500), BlurImage()], format="JPEG", options={"quality": 100}
    )

    isFromEditor = models.BooleanField(verbose_name=_("Is from editor"), default=False)

    def __str__(self):
        return self.name or self.image.name

    def get_image_url(self, field_name):
        file_obj = getattr(self, field_name)
        try:
            if not file_obj:
                return None
        except FileNotFoundError as e:
            logger.error("File does not exist on filesystem ", exc_info=e)
            return None
        return file_obj.url

    def save(self, *args, **kwargs):
        if not self.name and self.image.name:
            self.name = self.image.name
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = _("Image")
        verbose_name_plural = _("Images")
