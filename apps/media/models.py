from apps.comments.models import Comment
from apps.generic.choices import AccessChoices
from apps.generic.models import GenericModelMixin, GenericModerateMixin
from ckeditor.fields import RichTextField
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.utils.translation import gettext_lazy as _
from model_utils import FieldTracker


class MediaFolder(GenericModelMixin, models.Model):
    creator = models.ForeignKey("users.User", verbose_name=_("Creator"), on_delete=models.CASCADE)
    name = models.CharField(_("Media Tag"), max_length=255)
    show_media = models.CharField(
        _("Show media"), choices=AccessChoices.ACCESS, default=AccessChoices.ACCESS_ONLY_FRIENDS, max_length=16
    )

    media = GenericRelation("media.Media")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Media Folder")
        verbose_name_plural = _("Media Folder")


def limit_choices_to_content_type():
    return (
        models.Q(app_label="media", model="mediafolder")
        | models.Q(app_label="groups", model="group")
        | models.Q(app_label="clubs", model="club")
        | models.Q(app_label="events", model="party")
    )


class Media(GenericModerateMixin, models.Model):
    TYPE_PHOTO = "photo"
    TYPE_VIDEO = "video"
    TYPES = ((TYPE_PHOTO, _("Photo")), (TYPE_VIDEO, _("Video")))

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
    title = models.CharField(_("Title"), max_length=255, null=True, blank=True)
    description = RichTextField(_("Description"), config_name="basic", null=True, blank=True)

    image = models.ForeignKey(
        "storage.Image", verbose_name=_("Image"), on_delete=models.SET_NULL, null=True, blank=True
    )
    video_code = models.TextField(_("Embed video code"), null=True, blank=True)

    hash_tags = ArrayField(models.CharField(max_length=255), verbose_name=_("Hash tags"), default=list)
    likes = models.ManyToManyField("users.User", verbose_name=_("Likes"), blank=True, related_name="like_media")
    views = models.PositiveIntegerField(_("Views"), default=0)

    media_type = models.CharField(_("Type"), max_length=16, choices=TYPES)

    comments = GenericRelation(Comment)

    fields_tracker = FieldTracker(fields=["status"])

    def get_title(self):
        title = self.title
        if not title and self.image:
            title = self.image.name
        return title

    @property
    def comments_count(self):
        return self.comments.filter(is_deleted=False).count()

    def __str__(self):
        return self.title or str(self.pk)

    class Meta:
        verbose_name = _("Media")
        verbose_name_plural = _("Media")
