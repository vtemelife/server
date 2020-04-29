import uuid

from django.db import models
from django.utils.translation import gettext_lazy as _


class GenericUUIDMixin(models.Model):
    id = models.UUIDField(db_column="uuid", primary_key=True, default=uuid.uuid4, editable=False)

    created_date = models.DateTimeField(_("Created date"), auto_now_add=True)
    updated_date = models.DateTimeField(_("Updated date"), auto_now=True)

    class Meta:
        abstract = True


class GenericModelMixin(GenericUUIDMixin):
    is_deleted = models.BooleanField(_("Is deleted"), db_index=True, default=False)

    class Meta:
        abstract = True
        ordering = ["created_date"]


class GenericModerateMixin(GenericModelMixin):
    STATUS_WAITING_MODERATION = "waiting"
    STATUS_APPROVED = "approved"
    STATUS_DECLINED = "declined"

    STATUSES = (
        (STATUS_WAITING_MODERATION, _("Waiting moderation")),
        (STATUS_APPROVED, _("Approved")),
        (STATUS_DECLINED, _("Declined")),
    )

    status = models.CharField(_("Status"), choices=STATUSES, max_length=32, db_index=True, null=True, blank=True)
    is_ban = models.BooleanField(_("Is ban"), db_index=True, default=False)

    class Meta:
        abstract = True
        ordering = ["created_date"]
