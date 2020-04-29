from apps.generic.models import GenericModelMixin, GenericModerateMixin
from ckeditor.fields import RichTextField
from django.contrib.postgres.fields import ArrayField, JSONField
from django.db import models
from django.utils.translation import gettext_lazy as _


class Game(GenericModerateMixin, models.Model):
    creator = models.ForeignKey("users.User", verbose_name=_("Creator"), on_delete=models.CASCADE)
    users = models.ManyToManyField(
        "users.User", verbose_name=_("Users"), related_name="user_games", blank=True, through="games.GameUser"
    )
    slug = models.SlugField(_("Slug"), max_length=150, db_index=True, unique=True)
    name = models.CharField(_("Name"), max_length=255)
    image = models.ForeignKey(
        "storage.Image", verbose_name=_("Image"), on_delete=models.SET_NULL, null=True, blank=True
    )
    description = RichTextField(_("Description"), config_name="basic")
    rules = RichTextField(_("Rules"), config_name="basic", null=True, blank=True)
    hash_tags = ArrayField(models.CharField(max_length=255), verbose_name=_("Hash tags"), default=list)

    likes = models.ManyToManyField("users.User", verbose_name=_("Likes"), blank=True, related_name="like_games")
    views = models.PositiveIntegerField(_("Views"), default=0)
    token = models.UUIDField(_("Token"), null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Game")
        verbose_name_plural = _("Games")


class GameUser(GenericModelMixin, models.Model):
    user = models.ForeignKey(
        "users.User", verbose_name=_("User"), on_delete=models.CASCADE, related_name="user_gameusers"
    )
    game = models.ForeignKey(Game, verbose_name=_("Game"), on_delete=models.CASCADE, related_name="game_gameusers")
    game_data = JSONField(_("Game data"), default=dict)

    class Meta:
        verbose_name = _("Game User")
        verbose_name_plural = _("Game Users")
        unique_together = ("user", "game")
