from apps.generic.models import GenericModelMixin
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils.translation import gettext_lazy as _
from mptt.models import MPTTModel, TreeForeignKey


def limit_choices_to_content_type():
    return (
        models.Q(app_label="posts", model="post")
        | models.Q(app_label="news", model="news")
        | models.Q(app_label="media", model="media")
        | models.Q(app_label="events", model="party")
    )


class Comment(GenericModelMixin, MPTTModel):
    content_type = models.ForeignKey(
        ContentType,
        verbose_name=_("Content type"),
        limit_choices_to=limit_choices_to_content_type,
        on_delete=models.CASCADE,
    )
    object_id = models.UUIDField(_("Object UUID"))
    content_object = GenericForeignKey("content_type", "object_id")
    content_object.short_description = _("Content object")

    parent = TreeForeignKey("self", on_delete=models.CASCADE, null=True, blank=True, related_name="children")

    creator = models.ForeignKey("users.User", verbose_name=_("Creator"), on_delete=models.CASCADE)
    likes = models.ManyToManyField("users.User", verbose_name=_("Likes"), blank=True, related_name="like_comments")
    comment = models.TextField(_("Comment"))

    @property
    def preview(self):
        return self.comment[:20] + "..."

    def __str__(self):
        return self.preview

    class Meta:
        verbose_name = _("Comment")
        verbose_name_plural = _("Comments")
        ordering = ["created_date"]
