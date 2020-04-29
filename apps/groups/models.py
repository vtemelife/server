from ckeditor.fields import RichTextField
from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.generic.choices import ComminityTypeChoices, ThemeChoices
from apps.generic.models import GenericModelMixin


class Group(GenericModelMixin, models.Model):
    creator = models.ForeignKey("users.User", verbose_name=_("Creator"), on_delete=models.CASCADE)
    moderators = models.ManyToManyField(
        "users.User", verbose_name=_("Moderators"), related_name="moderator_groups", blank=True
    )
    users = models.ManyToManyField("users.User", verbose_name=_("Users"), related_name="user_groups", blank=True)

    name = models.CharField(_("Name"), max_length=255, unique=True, db_index=True)
    slug = models.SlugField(_("Slug"), max_length=150, db_index=True, unique=True)
    image = models.ForeignKey(
        "storage.Image", verbose_name=_("Image"), on_delete=models.SET_NULL, null=True, blank=True
    )
    description = RichTextField(_("Description"), config_name="basic", null=True, blank=True)

    group_type = models.CharField(_("Type"), max_length=16, choices=ComminityTypeChoices.TYPES, db_index=True)
    relationship_theme = models.CharField(
        _("Relationship themes"), choices=ThemeChoices.THEMES, max_length=16, db_index=True
    )
    raiting = models.PositiveIntegerField(_("Raiting"), default=0)

    requests = GenericRelation("memberships.MembershipRequest")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Group")
        verbose_name_plural = _("Groups")
