from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import BlackList


@receiver(post_save, sender=BlackList)
def _black_list_post_save(sender, instance, **kwargs):
    if instance.is_deleted:
        instance.delete()
