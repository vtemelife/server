from ckeditor.fields import RichTextField
from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.generic.models import GenericModelMixin


class Shop(GenericModelMixin, models.Model):
    creator = models.ForeignKey("users.User", verbose_name=_("Creator"), on_delete=models.CASCADE)
    moderators = models.ManyToManyField(
        "users.User", verbose_name=_("Moderators"), related_name="moderator_shops", blank=True
    )

    avatar = models.ForeignKey(
        "storage.Image", verbose_name=_("Avatar"), on_delete=models.SET_NULL, null=True, blank=True
    )
    name = models.CharField(_("Name"), max_length=255, unique=True)
    description = RichTextField(_("Description"), config_name="basic", null=True, blank=True)

    raiting = models.PositiveIntegerField(_("Raiting"), default=0)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Shop")
        verbose_name_plural = _("Shops")


class ShopItem(GenericModelMixin, models.Model):
    shop = models.ForeignKey(Shop, verbose_name=_("Shop"), on_delete=models.CASCADE)
    image = models.ForeignKey(
        "storage.Image", verbose_name=_("Image"), on_delete=models.SET_NULL, null=True, blank=True
    )
    name = models.CharField(_("Name"), max_length=255, unique=True)
    description = RichTextField(_("Description"), config_name="basic", null=True, blank=True)
    price = models.DecimalField(_("Price"), max_digits=5, decimal_places=2)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Item")
        verbose_name_plural = _("Items")
