from rest_framework import serializers

from apps.chat.models import Chat
from apps.generic.choices import ThemeChoices
from apps.generic.fields import ChoiceDisplayField
from apps.users.models import User
from apps.users.serializers.profile import UserSerializer


class ChatParticipantSerializer(UserSerializer):
    pass


class FriendSearchSerializer(UserSerializer):
    role = ChoiceDisplayField(choices=User.ROLES)
    gender = ChoiceDisplayField(choices=User.GENDERS)
    relationship_formats = ChoiceDisplayField(choices=User.FORMATS)
    relationship_themes = ChoiceDisplayField(choices=ThemeChoices.THEMES)
    request = serializers.SerializerMethodField()
    chat = serializers.SerializerMethodField()

    def get_request(self, obj):
        user = self.context["request"].user
        request = obj.requests.filter(user=user).first()
        if request:
            return request.pk

    def get_chat(self, obj):
        user = self.context["request"].user
        if user == obj:
            return
        chat = Chat.objects.user_chats(user).filter(chat_type=Chat.TYPE_CONVERSATION, users=obj).first()
        if chat:
            return chat.pk

    class Meta:
        model = User
        fields = (
            "pk",
            "slug",
            "name",
            "avatar",
            "online",
            "last_seen",
            "city",
            "about",
            "role",
            "gender",
            "relationship_formats",
            "relationship_themes",
            "birthday",
            "birthday_second",
            "is_real",
            "request",
            "chat",
        )


class FriendListItemSerializer(UserSerializer):
    chat = serializers.SerializerMethodField()

    def get_chat(self, obj):
        user = self.context["request"].user
        if user == obj:
            return
        chat = Chat.objects.user_chats(user).filter(chat_type=Chat.TYPE_CONVERSATION, users=obj).first()
        if chat:
            return chat.pk

    class Meta:
        model = User
        fields = ("pk", "slug", "name", "avatar", "online", "last_seen", "city", "about", "role", "chat")


class FriendDeleteSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("pk",)
