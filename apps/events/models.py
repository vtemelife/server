from cities_light.models import City
from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField
from django.contrib.contenttypes.fields import GenericRelation
from django.contrib.postgres.fields import ArrayField, JSONField
from django.db import models
from django.utils.translation import gettext_lazy as _
from model_utils import FieldTracker

from apps.clubs.models import Club
from apps.comments.models import Comment
from apps.generic.choices import ComminityTypeChoices, ThemeChoices
from apps.generic.models import GenericModerateMixin
from apps.users.models import User


class Party(GenericModerateMixin, models.Model):
    club = models.ForeignKey(Club, verbose_name=_("Club"), on_delete=models.CASCADE)

    name = models.CharField(_("Name"), max_length=255)
    slug = models.SlugField(_("Slug"), max_length=150, db_index=True, unique=True)
    image = models.ForeignKey(
        "storage.Image", verbose_name=_("Image"), on_delete=models.SET_NULL, null=True, blank=True
    )
    short_description = RichTextField(_("Short description"), config_name="basic")
    description = RichTextUploadingField(_("Description"), config_name="basic")

    city = models.ForeignKey(City, verbose_name=_("City"), on_delete=models.CASCADE, null=True)
    address = RichTextUploadingField(_("Address"), config_name="basic")
    geo = JSONField(_("Geo"), null=True, blank=True)
    start_date = models.DateTimeField(_("Start date"))
    end_date = models.DateTimeField(_("End date"))

    party_type = models.CharField(_("Type"), max_length=16, choices=ComminityTypeChoices.TYPES, db_index=True)
    theme = models.CharField(_("Theme"), max_length=16, choices=ThemeChoices.THEMES, db_index=True)
    hash_tags = ArrayField(models.CharField(max_length=255), verbose_name=_("Hash tags"), default=list)
    likes = models.ManyToManyField("users.User", verbose_name=_("Likes"), blank=True, related_name="like_parties")
    views = models.PositiveIntegerField(_("Views"), default=0)

    man_cost = models.FloatField(_("Man cost"), default=0)
    woman_cost = models.FloatField(_("Woman cost"), default=0)
    pair_cost = models.FloatField(_("Pair cost"), default=0)

    comments = GenericRelation(Comment)

    fields_tracker = FieldTracker(fields=["status"])

    @property
    def comments_count(self):
        return self.comments.filter(is_deleted=False).count()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Party")
        verbose_name_plural = _("Parties")


class PartyUser(models.Model):
    STATUS_UNKNOWN = "unknown"
    STATUS_NO = "no"
    STATUS_YES = "yes"
    STATUS_PROBABLY = "probably"

    STATUSES = ((STATUS_NO, _("No")), (STATUS_YES, _("Yes")), (STATUS_PROBABLY, _("Probably")))
    user = models.ForeignKey(User, verbose_name=_("User"), on_delete=models.CASCADE)
    party = models.ForeignKey(Party, verbose_name=_("Party"), on_delete=models.CASCADE)
    status = models.CharField(_("Theme"), max_length=16, choices=STATUSES)

    class Meta:
        verbose_name = _("Party User")
        verbose_name_plural = _("Party Users")
