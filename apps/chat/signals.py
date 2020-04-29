from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone

from .models import Chat, Message


@receiver(post_save, sender=Message)
def _message_post_save(sender, instance, created, **kwargs):
    if created:
        Chat.objects.filter(pk=instance.chat_id).update(updated_date=timezone.now())
