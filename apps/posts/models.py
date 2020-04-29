from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.utils.translation import gettext_lazy as _
from model_utils import FieldTracker

from apps.comments.models import Comment
from apps.generic.models import GenericModerateMixin


def limit_choices_to_content_type():
    return (
        models.Q(app_label="users", model="user")
        | models.Q(app_label="groups", model="group")
        | models.Q(app_label="clubs", model="club")
    )


class Post(GenericModerateMixin, models.Model):
    THEME_SWING = "swing"
    THEME_SWING_HISTORY = "swing_history"
    THEME_BDSM = "bdsm"
    THEME_BDSM_HISTORY = "bdsm_history"
    THEME_LGBT = "lgbt"
    THEME_LGBT_HISTORY = "lgbt_history"
    THEME_SEX = "sex"
    THEME_SEX_HISTORY = "sex_history"

    THEME_RULE = "rule"
    THEME_RULE_MEDIA = "rule_media"
    THEME_ADVERTISMENT = "advertisment"

    THEMES = (
        (THEME_SWING, _("Swing")),
        (THEME_SWING_HISTORY, _("Swing History")),
        (THEME_BDSM, _("Bdsm")),
        (THEME_BDSM_HISTORY, _("Bdsm History")),
        (THEME_LGBT, _("Lgbt")),
        (THEME_LGBT_HISTORY, _("Lgbt History")),
        (THEME_SEX, _("Sex")),
        (THEME_SEX_HISTORY, _("Sex History")),
        (THEME_RULE, _("Rule")),
        (THEME_RULE_MEDIA, _("Rule Media")),
        (THEME_ADVERTISMENT, _("Advertisment")),
    )

    content_type = models.ForeignKey(
        ContentType,
        verbose_name=_("Content type"),
        limit_choices_to=limit_choices_to_content_type,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    object_id = models.UUIDField(_("Object UUID"), null=True, blank=True)
    content_object = GenericForeignKey("content_type", "object_id")
    content_object.short_description = _("Content object")

    creator = models.ForeignKey("users.User", verbose_name=_("Creator"), on_delete=models.CASCADE)
    is_whisper = models.BooleanField(verbose_name=_("Is Whisper"), default=False)

    theme = models.CharField(_("Theme"), max_length=64, choices=THEMES, null=True, blank=True)
    hash_tags = ArrayField(models.CharField(max_length=255), verbose_name=_("Hash tags"), default=list)
    likes = models.ManyToManyField("users.User", verbose_name=_("Likes"), blank=True, related_name="like_posts")
    views = models.PositiveIntegerField(_("Views"), default=0)
    title = models.CharField(_("Title"), max_length=255)
    slug = models.SlugField(_("Slug"), max_length=150, db_index=True, unique=True)
    image = models.ForeignKey(
        "storage.Image", verbose_name=_("Image"), on_delete=models.SET_NULL, null=True, blank=True
    )
    description = RichTextField(_("Description"), config_name="basic")
    post = RichTextUploadingField(_("Post"), config_name="basic")

    comments = GenericRelation(Comment)

    fields_tracker = FieldTracker(fields=["status"])

    @property
    def comments_count(self):
        return self.comments.filter(is_deleted=False).count()

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _("Post")
        verbose_name_plural = _("Posts")
