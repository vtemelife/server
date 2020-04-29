from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import GameUser


@receiver(post_save, sender=GameUser)
def _game_user_post_save(sender, instance, **kwargs):
    if instance.is_deleted:
        instance.delete()
