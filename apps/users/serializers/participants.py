from apps.chat.models import Chat
from apps.users.models import User
from apps.users.serializers.profile import UserSerializer
from rest_framework import serializers


class ParticipantListItemSerializer(UserSerializer):
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
        fields = ("pk", "slug", "avatar", "name", "online", "city", "about", "role", "chat")
