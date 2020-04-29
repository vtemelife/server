from apps.users.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


def auto_moderate_user_guest(user):
    if user.role != User.ROLE_GUEST:
        return

    if user.avatar and user.about:
        User.objects.filter(pk=user.pk).update(role=User.ROLE_MEMBER, status=User.STATUS_APPROVED)


@receiver(post_save, sender=User)
def _user_post_save(sender, instance, **kwargs):
    auto_moderate_user_guest(instance)
