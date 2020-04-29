from django.contrib.contenttypes.models import ContentType
from django.db import transaction
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from django.utils.translation import gettext as _

from apps.events.models import Party, PartyUser
from apps.generic.choices import AccessChoices, ThemeChoices
from apps.media.models import Media
from apps.news.models import News
from apps.posts.models import Post
from apps.users.models import User


@receiver(post_save, sender=User)
def _user_post_save(sender, instance, created, **kwargs):
    if instance.is_deleted:
        News.objects.filter(object_id=instance.id, content_type=ContentType.objects.get_for_model(instance)).update(
            is_deleted=True
        )
        return

    fields_changes = list(instance.fields_tracker.changed().keys())
    if not created and fields_changes:
        news_type = News.TYPE_FRIENDS_INFO
        recipients_pks = list(instance.friends.filter(is_active=True, is_deleted=False).values_list("pk", flat=True))
        if recipients_pks and news_type:
            description = _("User has updated the fields %s") % ", ".join(
                [str(User._meta.get_field(f).verbose_name) for f in fields_changes]
            )
            with transaction.atomic():
                news = News.objects.create(
                    content_object=instance,
                    news_type=news_type,
                    creator=instance,
                    image=instance.avatar,
                    description=description,
                    publish_date=timezone.now(),
                    slug=instance.slug,
                )
                news.recipients.set(recipients_pks)


@receiver(post_save, sender=Media)
def _media_post_save(sender, instance, created, **kwargs):
    if instance.is_deleted:
        News.objects.filter(object_id=instance.id, content_type=ContentType.objects.get_for_model(instance)).update(
            is_deleted=True
        )
        return

    if instance.fields_tracker.has_changed("status") and instance.status == Media.STATUS_APPROVED:
        News.objects.create(
            content_object=instance,
            news_type=News.TYPE_MEDIA,
            creator=instance.creator,
            image=instance.image,
            title=instance.get_title(),
            description=instance.description,
            publish_date=timezone.now(),
        )

    if created:
        creator = instance.creator
        parent = instance.content_object
        parent_cls = parent.__class__.__name__
        if parent_cls not in ("MediaFolder", "Group", "Club"):
            return

        theme = None
        news_type = None
        recipients_pks = []
        if parent_cls == "MediaFolder":
            if parent.show_media == AccessChoices.ACCESS_NO_USERS:
                return
            news_type = News.TYPE_FRIENDS_MEDIA
            recipients_pks = list(creator.friends.filter(is_active=True, is_deleted=False).values_list("pk", flat=True))
        elif parent_cls == "Group":
            news_type = News.TYPE_GROUPS_MEDIA
            theme = parent.relationship_theme
            recipients_pks = list(parent.users.filter(is_active=True, is_deleted=False).values_list("pk", flat=True))
        elif parent_cls == "Club":
            news_type = News.TYPE_CLUBS_MEDIA
            theme = parent.relationship_theme
            recipients_pks = list(parent.users.filter(is_active=True, is_deleted=False).values_list("pk", flat=True))

        if recipients_pks and news_type:
            with transaction.atomic():
                news = News.objects.create(
                    content_object=instance,
                    news_type=news_type,
                    creator=instance.creator,
                    image=instance.image,
                    title=instance.title,
                    description=instance.description,
                    publish_date=timezone.now(),
                    theme=theme,
                )
                news.recipients.set(recipients_pks)


@receiver(post_save, sender=Post)
def _article_post_save(sender, instance, created, **kwargs):
    if instance.is_deleted:
        News.objects.filter(object_id=instance.id, content_type=ContentType.objects.get_for_model(instance)).update(
            is_deleted=True
        )
        return

    theme = None
    if instance.theme in (Post.THEME_BDSM, Post.THEME_BDSM_HISTORY):
        theme = ThemeChoices.THEME_BDSM
    elif instance.theme in (Post.THEME_LGBT, Post.THEME_LGBT_HISTORY):
        theme = ThemeChoices.THEME_LGBT
    elif instance.theme in (Post.THEME_SWING, Post.THEME_SWING_HISTORY):
        theme = ThemeChoices.THEME_SWING

    if instance.fields_tracker.has_changed("status") and instance.status == Post.STATUS_APPROVED:
        News.objects.create(
            content_object=instance,
            news_type=News.TYPE_WHISPER if instance.is_whisper else News.TYPE_ARTICLES,
            creator=instance.creator,
            image=instance.image,
            title=instance.title,
            description=instance.description,
            publish_date=timezone.now(),
            slug=instance.slug,
            theme=theme,
        )

    if created:
        creator = instance.creator
        parent = instance.content_object
        parent_cls = parent.__class__.__name__
        if parent_cls not in ("User", "Group", "Club"):
            return

        news_type = None
        recipients_pks = []
        if parent_cls == "User":
            news_type = News.TYPE_FRIENDS_ARTICLE
            recipients_pks = list(creator.friends.filter(is_active=True, is_deleted=False).values_list("pk", flat=True))
        elif parent_cls == "Group":
            news_type = News.TYPE_GROUPS_ARTICLE
            recipients_pks = list(parent.users.filter(is_active=True, is_deleted=False).values_list("pk", flat=True))
        elif parent_cls == "Club":
            news_type = News.TYPE_CLUBS_ARTICLE
            recipients_pks = list(parent.users.filter(is_active=True, is_deleted=False).values_list("pk", flat=True))

        if recipients_pks and news_type:
            with transaction.atomic():
                news = News.objects.create(
                    content_object=instance,
                    news_type=news_type,
                    creator=instance.creator,
                    image=instance.image,
                    title=instance.title,
                    description=instance.description,
                    publish_date=timezone.now(),
                    slug=instance.slug,
                    theme=theme,
                )
                news.recipients.set(recipients_pks)


@receiver(post_save, sender=Party)
def _party_post_save(sender, instance, created, **kwargs):
    if instance.is_deleted:
        News.objects.filter(object_id=instance.id, content_type=ContentType.objects.get_for_model(instance)).update(
            is_deleted=True
        )
        return

    if instance.fields_tracker.has_changed("status") and instance.status == Post.STATUS_APPROVED:
        parent = instance.club
        news_type = None
        recipients_pks = []
        news_type = News.TYPE_CLUBS_EVENTS
        recipients_pks = list(parent.users.filter(is_active=True, is_deleted=False).values_list("pk", flat=True))
        recipients_pks += list(PartyUser.objects.filter(party=instance).values_list("user_id", flat=True))
        recipients_pks = list(set(recipients_pks))

        if recipients_pks and news_type:
            with transaction.atomic():
                news = News.objects.create(
                    content_object=instance,
                    news_type=news_type,
                    creator=instance.club.creator,
                    image=instance.image,
                    title=instance.name,
                    description=instance.short_description,
                    publish_date=timezone.now(),
                    slug=instance.slug,
                    theme=instance.theme,
                )
                news.recipients.set(recipients_pks)
