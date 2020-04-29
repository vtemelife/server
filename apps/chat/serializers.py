import datetime

from apps.storage.serializers import ImageSerializer
from apps.users.serializers.friends import ChatParticipantSerializer
from apps.users.serializers.profile import UserSerializer
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from .models import Chat, ChatBan, Message


class ChatMixin:
    def _get_users_fields(self, obj, field_name):
        current_user = self.context["request"].user
        return [
            getattr(user, field_name)
            for user in obj.users.filter(is_active=True, is_deleted=False)
            if user.pk != current_user.pk
        ]

    def get_name(self, obj):
        return obj.get_chat_name(current_user=self.context["request"].user)

    def get_avatar(self, obj):
        avatar = obj.get_chat_avatar(current_user=self.context["request"].user)
        serializer = ImageSerializer(avatar, context=self.context)
        return serializer.data


class ChatListSerializer(ChatMixin, serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    avatar = serializers.SerializerMethodField()
    moderators = serializers.SerializerMethodField()

    messages_count = serializers.SerializerMethodField()
    unread_messages_count = serializers.SerializerMethodField()
    last_message = serializers.SerializerMethodField()

    def get_moderators(self, obj):
        return obj.get_chat_moderators().values_list("pk", flat=True)

    def get_messages_count(self, obj):
        return Message.objects.filter(chat=obj.pk).count()

    def get_unread_messages_count(self, obj):
        user = self.context["request"].user
        return Message.objects.filter(chat=obj.pk).exclude(viewed_by=user).count()

    def get_last_message(self, obj):
        serializer = MessageListSerializer(obj.get_last_message(), context=self.context)
        return serializer.data

    class Meta:
        model = Chat
        fields = (
            "pk",
            "name",
            "avatar",
            "updated_date",
            "messages_count",
            "unread_messages_count",
            "creator",
            "moderators",
            "chat_type",
            "last_message",
        )


class ChatRetrieveSerializer(ChatMixin, serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    avatar = serializers.SerializerMethodField()
    moderators = serializers.SerializerMethodField()

    users = ChatParticipantSerializer(many=True)

    def get_moderators(self, obj):
        serializer = UserSerializer(obj.get_chat_moderators(), many=True, context=self.context)
        return serializer.data

    class Meta:
        model = Chat
        fields = ("pk", "name", "avatar", "creator", "moderators", "users", "bans", "chat_type")


class ChatConversationCreateSerializer(serializers.ModelSerializer):
    recipient = serializers.SlugField(write_only=True)
    message = serializers.CharField(write_only=True)

    class Meta:
        model = Chat
        fields = ("pk", "recipient", "message")


class ChatCreateSerializer(serializers.ModelSerializer):
    message = serializers.CharField(write_only=True)

    class Meta:
        model = Chat
        fields = ("pk", "name", "users", "message")


class ChatWithModeratorsCreateSerializer(serializers.ModelSerializer):
    message = serializers.CharField(write_only=True)

    class Meta:
        model = Chat
        fields = ("pk", "name", "message")


class ChatUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chat
        fields = ("pk", "name", "avatar", "moderators", "users")


class ChatDeleteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chat
        fields = ("pk",)


class ChatLeaveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chat
        fields = ("pk",)


class ChatBanUserSerializer(serializers.ModelSerializer):
    user = serializers.UUIDField(write_only=True)
    minutes = serializers.IntegerField(write_only=True)

    class Meta:
        model = Chat
        fields = ("pk", "user", "minutes")


class ChatBlockUserSerializer(serializers.ModelSerializer):
    user = serializers.UUIDField(write_only=True)

    class Meta:
        model = Chat
        fields = ("pk", "user")


class MessageListSerializer(serializers.ModelSerializer):
    creator = UserSerializer(read_only=True)
    attachments_data = serializers.SerializerMethodField()

    def get_attachments_data(self, obj):
        serializer = ImageSerializer(obj.attachments.all(), many=True, context=self.context)
        return serializer.data

    class Meta:
        model = Message
        fields = ("pk", "message", "creator", "attachments_data", "created_date")


class MessageCreateSerializer(MessageListSerializer):
    def validate(self, data):
        data = super().validate(data)
        if not data.get("message") and not data.get("attachments"):
            raise serializers.ValidationError({"message": [_("Please write your message")]})
        return data

    def create(self, validated_data):
        user = self.context["request"].user
        chat = validated_data["chat"]
        ban = ChatBan.objects.filter(user=user, chat=chat).first()
        if ban and timezone.now() <= (ban.ban_date + datetime.timedelta(minutes=ban.minutes)):
            error = _(
                "Your have been baned for {minutes} minutes. " "Please contact with moderators of the chat."
            ).format(minutes=ban.minutes)
            raise serializers.ValidationError({"message": [error]})
        if chat.chat_type == Chat.TYPE_CONVERSATION:
            if chat.users.exclude(pk=user.pk).filter(black_list__pk=user.pk).distinct().exists():
                error = _("You cannot send a message to this user cause you are in user's black list")
                raise serializers.ValidationError({"message": [error]})
        return super().create(validated_data)

    class Meta:
        model = Message
        fields = ("pk", "chat", "message", "creator", "attachments_data", "attachments", "created_date")


class MessageUpdateSerializer(MessageCreateSerializer):
    class Meta:
        model = Message
        fields = ("pk", "message", "attachments")


class MessageDeleteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ("pk",)
