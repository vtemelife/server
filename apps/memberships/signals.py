from django.contrib.contenttypes.models import ContentType
from django.db.models.signals import post_save
from django.dispatch import receiver

from apps.clubs.models import Club
from apps.groups.models import Group
from apps.users.models import User

from .models import MembershipRequest


@receiver(post_save, sender=MembershipRequest)
def _membership_request_post_save(sender, instance, **kwargs):
    if instance.status == MembershipRequest.STATUS_APPROVED:
        ct_user = ContentType.objects.get_for_model(User)
        ct_group = ContentType.objects.get_for_model(Group)
        ct_club = ContentType.objects.get_for_model(Club)
        if instance.content_type == ct_user:
            instance.user.friends.add(instance.object_id)
            instance.content_object.friends.add(instance.user_id)
        if instance.content_type == ct_group:
            instance.content_object.users.add(instance.user_id)
        if instance.content_type == ct_club:
            instance.content_object.users.add(instance.user_id)

    if instance.is_deleted:
        instance.delete()
