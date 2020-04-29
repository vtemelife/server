from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.generic.models import GenericModerateMixin
from apps.users.models import User


def limit_choices_to_content_type():
    return (
        models.Q(app_label="users", model="user")
        | models.Q(app_label="groups", model="group")
        | models.Q(app_label="clubs", model="club")
        | models.Q(app_label="events", model="event")
    )


class MembershipRequest(GenericModerateMixin, models.Model):
    user = models.ForeignKey(User, verbose_name=_("User"), related_name="membership_requests", on_delete=models.CASCADE)

    content_type = models.ForeignKey(
        ContentType,
        verbose_name=_("Content type"),
        limit_choices_to=limit_choices_to_content_type,
        on_delete=models.CASCADE,
    )
    object_id = models.UUIDField(_("Object UUID"))
    content_object = GenericForeignKey("content_type", "object_id")
    content_object.short_description = _("Content object")

    def __str__(self):
        return "{}: {}".format(self.user, self.content_object)

    class Meta:
        verbose_name = _("Membership request")
        verbose_name_plural = _("Membership requests")
        unique_together = ("user", "content_type", "object_id")
