from apps.generic.models import GenericModelMixin, GenericUUIDMixin
from django.db import models
from django.utils.translation import gettext_lazy as _


class ChatQuerySet(models.QuerySet):
    def user_chats(self, user, is_moderator=None):
        qs = self.filter(is_deleted=False, users=user)
        if not is_moderator:
            qs = qs.exclude(models.Q(chat_type=Chat.TYPE_CHAT_WITH_MODERATORS) & ~models.Q(creator=user))
        else:
            qs = qs.filter(chat_type=Chat.TYPE_CHAT_WITH_MODERATORS)
        return qs

    def unread(self, user):
        return self.filter(pk__in=Message.objects.exclude(viewed_by=user).values_list("chat_id", flat=True)).distinct()


class Chat(GenericModelMixin, models.Model):
    TYPE_CHAT = "chat"
    TYPE_CONVERSATION = "conversation"
    TYPE_CHAT_WITH_MODERATORS = "chat_with_moderators"
    TYPES = (
        (TYPE_CHAT, _("Chat")),
        (TYPE_CONVERSATION, _("Conversation")),
        (TYPE_CHAT_WITH_MODERATORS, _("Chat with moderators")),
    )

    name = models.CharField(_("Name"), max_length=255, null=True, blank=True, db_index=True)
    avatar = models.ForeignKey(
        "storage.Image", verbose_name=_("Avatar"), on_delete=models.SET_NULL, null=True, blank=True
    )

    chat_type = models.CharField(_("Chat type"), max_length=64, choices=TYPES, default=TYPE_CHAT, db_index=True)

    creator = models.ForeignKey("users.User", verbose_name=_("Creator"), on_delete=models.CASCADE)
    moderators = models.ManyToManyField(
        "users.User", verbose_name=_("Moderators"), related_name="moderator_chats", blank=True
    )
    users = models.ManyToManyField("users.User", verbose_name=_("Users"), related_name="user_chats", blank=True)

    bans = models.ManyToManyField(
        "users.User", verbose_name=_("Users"), related_name="user_chat_bans", blank=True, through="chat.ChatBan"
    )

    objects = ChatQuerySet.as_manager()

    @property
    def chat_name(self):
        return str(self)

    def ban(self, user_id, minutes):
        ChatBan.objects.get_or_create(chat=self, user_id=user_id, minutes=minutes)

    def block(self, user_id):
        self.moderators.remove(user_id)
        self.users.remove(user_id)

    def leave(self, user):
        self.users.remove(user)
        Message.objects.create(chat=self, creator=user, message=_("User {} has been left the chat".format(user.name)))
        ChatBan.objects.filter(user=user, chat=self).delete()

    def get_recipients(self, sender=None):
        qs = self.users.all()
        sender_user = sender or self.creator
        qs = qs.exclude(pk=sender_user.pk)
        return list(qs.values_list("name", flat=True))

    def get_last_message(self):
        return self.chat_messages.filter(is_deleted=False).order_by("created_date").last()

    def get_chat_name(self, current_user):
        if self.name:
            return self.name
        recipients = self.get_recipients(sender=current_user)
        if self.chat_type == self.TYPE_CHAT:
            return ",".join(recipients)
        if self.chat_type == self.TYPE_CONVERSATION:
            return ",".join(recipients)
        if self.chat_type == self.TYPE_CHAT_WITH_MODERATORS:
            return _("Chat with moderators")
        return _("Chat")

    def get_chat_avatar(self, current_user):
        if self.avatar:
            return self.avatar
        if self.chat_type == self.TYPE_CONVERSATION:
            qs = self.users.filter(is_active=True, is_deleted=False)
            recipient = qs.exclude(pk=current_user.pk).first()
            if recipient:
                return recipient.avatar
        return None

    def get_chat_moderators(self):
        if self.chat_type == self.TYPE_CONVERSATION:
            return self.moderators.none()
        return self.moderators.filter(is_active=True, is_deleted=False)

    def __str__(self):
        return "{creator} - {recipients}".format(creator=self.creator.name, recipients=self.get_recipients())

    class Meta:
        verbose_name = _("Chat")
        verbose_name_plural = _("Chats")


class ChatBan(GenericUUIDMixin, models.Model):
    chat = models.ForeignKey(Chat, verbose_name=_("Chat"), on_delete=models.CASCADE, related_name="chat_chatbans")
    user = models.ForeignKey(
        "users.User", verbose_name=_("User"), on_delete=models.CASCADE, related_name="user_chatbans"
    )
    minutes = models.PositiveIntegerField(_("Ban minutes"), default=5)
    ban_date = models.DateTimeField(_("Ban date"), auto_now_add=True)

    class Meta:
        verbose_name = _("Chat Ban")
        verbose_name_plural = _("Chat Bans")
        unique_together = ("chat", "user")


class MessageQuerySet(models.QuerySet):
    def do_read(self, user):
        for message in self.exclude(viewed_by=user).distinct():
            message.do_read(user)


class Message(GenericModelMixin, models.Model):
    chat = models.ForeignKey(Chat, verbose_name=_("Chat"), on_delete=models.CASCADE, related_name="chat_messages")

    message = models.TextField(_("Message"), null=True, blank=True)

    creator = models.ForeignKey(
        "users.User", verbose_name=_("Creator"), on_delete=models.CASCADE, related_name="creator_messages"
    )
    viewed_by = models.ManyToManyField(
        "users.User", verbose_name=_("Viewed by"), related_name="user_viewed_chats", blank=True
    )

    attachments = models.ManyToManyField(
        "storage.Image", verbose_name=_("Attachments"), related_name="attachmnets_chats", blank=True
    )

    objects = MessageQuerySet.as_manager()

    @property
    def preview(self):
        return self.message[:20] + "..."

    def do_read(self, user):
        self.viewed_by.add(user)

    def __str__(self):
        return self.preview

    class Meta:
        verbose_name = _("Message")
        verbose_name_plural = _("Messages")
        ordering = ["chat__created_date", "created_date"]
