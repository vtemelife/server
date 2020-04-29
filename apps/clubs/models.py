from apps.generic.choices import ComminityTypeChoices, ThemeChoices
from apps.generic.models import GenericModerateMixin
from cities_light.models import City
from ckeditor.fields import RichTextField
from django.contrib.contenttypes.fields import GenericRelation
from django.contrib.postgres.fields import JSONField
from django.db import models
from django.utils.translation import gettext_lazy as _


class Club(GenericModerateMixin, models.Model):
    creator = models.ForeignKey("users.User", verbose_name=_("Creator"), on_delete=models.CASCADE)
    moderators = models.ManyToManyField(
        "users.User", verbose_name=_("Moderators"), related_name="moderator_clubs", blank=True
    )
    users = models.ManyToManyField("users.User", verbose_name=_("Users"), related_name="user_clubs", blank=True)

    name = models.CharField(_("Name"), max_length=255, unique=True, db_index=True)
    slug = models.SlugField(_("Slug"), max_length=150, db_index=True, unique=True)
    image = models.ForeignKey(
        "storage.Image", verbose_name=_("Image"), on_delete=models.SET_NULL, null=True, blank=True
    )
    description = RichTextField(_("Description"), config_name="basic", null=True, blank=True)

    club_type = models.CharField(_("Type"), max_length=16, choices=ComminityTypeChoices.TYPES, db_index=True)

    relationship_theme = models.CharField(
        _("Relationship themes"), choices=ThemeChoices.THEMES, max_length=16, db_index=True
    )
    raiting = models.PositiveIntegerField(_("Raiting"), default=0)

    city = models.ForeignKey(City, verbose_name=_("City"), on_delete=models.CASCADE, null=True)
    address = models.TextField(verbose_name=_("Address"), null=True)
    geo = JSONField(_("Geo"), null=True, blank=True)

    requests = GenericRelation("memberships.MembershipRequest")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Club")
        verbose_name_plural = _("Clubs")
