from apps.users.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Club


@receiver(post_save, sender=Club)
def _club_post_save(sender, instance, **kwargs):
    if instance.status == Club.STATUS_APPROVED and instance.creator.role == User.ROLE_MEMBER:
        instance.creator.role = User.ROLE_ORGANIZER
        instance.creator.save(update_fields=("role",))
