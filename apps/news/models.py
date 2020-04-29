from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.db.models import Q
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from apps.comments.models import Comment
from apps.generic.choices import ThemeChoices
from apps.generic.models import GenericModelMixin


def limit_choices_to_content_type():
    return (
        models.Q(app_label="media", model="media")
        | models.Q(app_label="groups", model="group")
        | models.Q(app_label="clubs", model="club")
        | models.Q(app_label="events", model="event")
    )


class NewsQuerySet(models.QuerySet):
    def do_read(self, user):
        for message in self.exclude(viewed_by=user).distinct():
            message.do_read(user)

    def unread(self, user):
        return self.exclude(viewed_by=user)

    def published(self):
        now = timezone.now()
        return self.filter(
            Q(publish_date__lte=now) & (Q(end_publish_date__gt=now) | Q(end_publish_date__isnull=True))
        ).distinct()

    def not_published(self):
        now = timezone.now()
        return self.filter(
            ~(Q(publish_date__lte=now) & (Q(end_publish_date__gt=now) | Q(end_publish_date__isnull=True)))
        ).distinct()


class News(GenericModelMixin, models.Model):
    TYPE_SITE_NEWS = "site_news"
    TYPE_MEDIA = "media"
    TYPE_ARTICLES = "articles"
    TYPE_WHISPER = "whisper"
    TYPE_FRIENDS_MEDIA = "friends_media"
    TYPE_FRIENDS_ARTICLE = "friends_article"
    TYPE_FRIENDS_INFO = "friends_info"
    TYPE_GROUPS_MEDIA = "groups_media"
    TYPE_GROUPS_ARTICLE = "groups_article"
    TYPE_CLUBS_MEDIA = "clubs_media"
    TYPE_CLUBS_ARTICLE = "clubs_article"
    TYPE_CLUBS_EVENTS = "clubs_events"
    TYPES = (
        (TYPE_SITE_NEWS, _("Hot News")),
        (TYPE_MEDIA, _("VTeme: New Media")),
        (TYPE_ARTICLES, _("VTeme: New Articles")),
        (TYPE_WHISPER, _("VTeme: New Whisper Articles")),
        (TYPE_FRIENDS_MEDIA, _("Friends: New Media")),
        (TYPE_FRIENDS_ARTICLE, _("Friends: New Articles")),
        (TYPE_FRIENDS_INFO, _("Friends: Profile Changes")),
        (TYPE_GROUPS_MEDIA, _("Groups: New Media")),
        (TYPE_GROUPS_ARTICLE, _("Groups: New Articles")),
        (TYPE_CLUBS_MEDIA, _("Clubs: New Media")),
        (TYPE_CLUBS_ARTICLE, _("Clubs: New Articles")),
        (TYPE_CLUBS_EVENTS, _("Clubs: Events")),
    )

    news_type = models.CharField(_("Type"), max_length=16, choices=TYPES)

    content_type = models.ForeignKey(
        ContentType,
        verbose_name=_("Content type"),
        limit_choices_to=limit_choices_to_content_type,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    object_id = models.UUIDField(_("Object UUID"), null=True, blank=True)
    content_object = GenericForeignKey("content_type", "object_id")
    content_object.short_description = _("Content object")
    slug = models.SlugField(_("Slug"), max_length=150, db_index=True, null=True, blank=True)

    creator = models.ForeignKey(
        "users.User", verbose_name=_("Creator"), on_delete=models.SET_NULL, null=True, blank=True
    )
    recipients = models.ManyToManyField(
        "users.User", verbose_name=_("Recipients"), blank=True, related_name="recipient_news"
    )
    viewed_by = models.ManyToManyField(
        "users.User", verbose_name=_("Viewed by"), related_name="user_viewed_news", blank=True
    )

    image = models.ForeignKey(
        "storage.Image", verbose_name=_("Image"), on_delete=models.SET_NULL, null=True, blank=True
    )

    title = models.CharField(_("Title"), max_length=255, null=True, blank=True)
    description = RichTextField(_("Description"), config_name="basic", null=True, blank=True)
    news = RichTextUploadingField(_("Post"), config_name="basic", null=True, blank=True)

    theme = models.CharField(_("Theme"), max_length=64, choices=ThemeChoices.THEMES, null=True, blank=True)

    publish_date = models.DateTimeField(_("Publish Date"), null=True, blank=True)
    end_publish_date = models.DateTimeField(_("End Publish Date"), null=True, blank=True)

    hash_tags = ArrayField(models.CharField(max_length=255), verbose_name=_("Hash tags"), default=list)
    likes = models.ManyToManyField("users.User", verbose_name=_("Likes"), blank=True, related_name="like_news")
    views = models.PositiveIntegerField(_("Views"), default=0)

    comments = GenericRelation(Comment)

    def do_read(self, user):
        self.viewed_by.add(user)

    @property
    def comments_count(self):
        return self.comments.filter(is_deleted=False).count()

    def __str__(self):
        return self.title or str(self.pk)

    objects = NewsQuerySet.as_manager()

    class Meta:
        verbose_name = _("News")
        verbose_name_plural = _("News")
