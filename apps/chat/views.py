from apps.generic.pagination import ReverseLimitOffsetPagination
from apps.generic.permissions import IsAuthenticatedAndActive, IsNotGuest
from apps.users.models import User
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404
from django.utils.translation import gettext_lazy as _
from rest_framework import generics, serializers
from rest_framework.response import Response

from .filtersets import ChatFilterSet, MessageFilterSet
from .models import Chat, Message
from .serializers import (
    ChatBanUserSerializer,
    ChatBlockUserSerializer,
    ChatConversationCreateSerializer,
    ChatCreateSerializer,
    ChatDeleteSerializer,
    ChatLeaveSerializer,
    ChatListSerializer,
    ChatRetrieveSerializer,
    ChatUpdateSerializer,
    ChatWithModeratorsCreateSerializer,
    MessageCreateSerializer,
    MessageDeleteSerializer,
    MessageListSerializer,
    MessageUpdateSerializer,
)


class ChatListView(generics.ListAPIView):
    serializer_class = ChatListSerializer
    queryset = Chat.objects.all().select_related("creator", "avatar").prefetch_related("moderators")
    filterset_class = ChatFilterSet
    search_fields = ("name", "users__slug", "users__name")
    permission_classes = (IsAuthenticatedAndActive,)
    is_moderator = False

    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.user_chats(self.request.user, is_moderator=self.is_moderator)
        return qs.order_by("-updated_date")


class ChatRetrieveView(generics.RetrieveAPIView):
    serializer_class = ChatRetrieveSerializer
    queryset = (
        Chat.objects.filter(is_deleted=False)
        .select_related("creator", "avatar")
        .prefetch_related("users", "moderators", "bans")
    )
    permission_classes = (IsAuthenticatedAndActive,)

    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.filter(users=self.request.user)
        return qs


class ChatConversationCreateView(generics.CreateAPIView):
    serializer_class = ChatConversationCreateSerializer
    permission_classes = (IsNotGuest,)

    def perform_create(self, serializer):
        recipient_slug = serializer.validated_data.pop("recipient")
        message = serializer.validated_data.pop("message")
        creator = self.request.user
        instance = serializer.save(creator=creator, chat_type=Chat.TYPE_CONVERSATION)
        recipient = get_object_or_404(User, slug=recipient_slug)
        instance.users.add(creator, recipient)
        message_obj = Message.objects.create(creator=creator, chat=instance, message=message)
        message_obj.do_read(creator)


class ChatCreateView(generics.CreateAPIView):
    serializer_class = ChatCreateSerializer
    permission_classes = (IsNotGuest,)

    def perform_create(self, serializer):
        message = serializer.validated_data.pop("message")
        creator = self.request.user
        instance = serializer.save(creator=creator, chat_type=Chat.TYPE_CHAT)
        instance.moderators.add(creator)
        instance.users.add(creator)
        message_obj = Message.objects.create(creator=creator, chat=instance, message=message)
        message_obj.do_read(creator)


class ChatWithModeratorsCreateView(generics.CreateAPIView):
    serializer_class = ChatWithModeratorsCreateSerializer
    permission_classes = (IsAuthenticatedAndActive,)

    def perform_create(self, serializer):
        message = serializer.validated_data.pop("message")
        creator = self.request.user
        instance = serializer.save(
            name=_("Chat with moderators ({name})").format(name=creator.name),
            creator=creator,
            chat_type=Chat.TYPE_CHAT_WITH_MODERATORS,
        )
        moderators = User.objects.filter(is_active=True, is_deleted=False, role=User.ROLE_MODERATOR)
        instance.moderators.add(creator, *moderators)
        instance.users.add(creator, *moderators)
        message_obj = Message.objects.create(creator=creator, chat=instance, message=message)
        message_obj.do_read(creator)


class ChatUpdateView(generics.UpdateAPIView):
    serializer_class = ChatUpdateSerializer
    queryset = Chat.objects.filter(is_deleted=False)
    permission_classes = (IsNotGuest,)

    def check_object_permissions(self, request, obj):
        if self.request.user.role == User.ROLE_MODERATOR:
            return
        if obj.chat_type != Chat.TYPE_CHAT:
            raise PermissionDenied
        if not obj.moderators.filter(pk=request.user.pk).exists():
            raise PermissionDenied


class ChatDeleteView(generics.UpdateAPIView):
    serializer_class = ChatDeleteSerializer
    queryset = Chat.objects.filter(is_deleted=False)
    permission_classes = (IsNotGuest,)

    def check_object_permissions(self, request, obj):
        if self.request.user.role == User.ROLE_MODERATOR:
            return
        if obj.chat_type != Chat.TYPE_CHAT:
            raise PermissionDenied
        if not obj.moderators.filter(pk=request.user.pk).exists():
            raise PermissionDenied

    def perform_update(self, serializer):
        serializer.save(is_deleted=True)


class ChatLeaveView(generics.UpdateAPIView):
    serializer_class = ChatLeaveSerializer
    queryset = Chat.objects.filter(is_deleted=False)
    permission_classes = (IsAuthenticatedAndActive,)

    def check_object_permissions(self, request, obj):
        if not obj.users.filter(pk=request.user.pk).exists():
            raise PermissionDenied

    def perform_update(self, serializer):
        instance = serializer.instance
        instance.leave(self.request.user)


class ChatBanUserView(generics.UpdateAPIView):
    serializer_class = ChatBanUserSerializer
    queryset = Chat.objects.filter(is_deleted=False)
    permission_classes = (IsNotGuest,)

    def check_object_permissions(self, request, obj):
        if obj.type == Chat.TYPE_CONVERSATION:
            raise PermissionDenied
        if self.request.user.role == User.ROLE_MODERATOR:
            return
        if not obj.moderators.filter(pk=request.user.pk).exists():
            raise PermissionDenied

    def perform_update(self, serializer):
        instance = serializer.instance
        instance.ban(serializer.validated_data["user"], serializer.validated_data["minutes"])


class ChatBlockUserView(generics.UpdateAPIView):
    serializer_class = ChatBlockUserSerializer
    queryset = Chat.objects.filter(is_deleted=False)
    permission_classes = (IsNotGuest,)

    def check_object_permissions(self, request, obj):
        if self.request.user.role == User.ROLE_MODERATOR:
            return
        if not obj.moderators.filter(pk=request.user.pk).exists():
            raise PermissionDenied

    def perform_update(self, serializer):
        instance = serializer.instance
        instance.block(serializer.validated_data["user"])


class ChatReadAll(generics.GenericAPIView):
    permission_classes = (IsAuthenticatedAndActive,)
    queryset = Chat.objects.filter(is_deleted=False)

    def get_serializer_class(self):
        return serializers.Serializer

    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.filter(users=self.request.user)
        return qs.unread(self.request.user)

    def post(self, request, *args, **kwargs):
        unread_chats = self.get_queryset()
        is_moderation_mode = bool(self.request.data.get("is_moderation_mode"))
        if is_moderation_mode:
            unread_chats = unread_chats.filter(chat_type=Chat.TYPE_CHAT_WITH_MODERATORS)
        else:
            unread_chats = unread_chats.exclude(chat_type=Chat.TYPE_CHAT_WITH_MODERATORS)
        unread_msgs = Message.objects.filter(chat__in=unread_chats)
        unread_msgs.do_read(self.request.user)
        return Response({})


class ChatMessagesReadAll(ChatReadAll):
    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.filter(pk=self.kwargs["pk"])
        return qs


class MessageListView(generics.ListAPIView):
    pagination_class = ReverseLimitOffsetPagination
    serializer_class = MessageListSerializer
    queryset = Message.objects.filter(is_deleted=False).prefetch_related("attachments")
    filterset_class = MessageFilterSet
    search_fields = ("message",)
    permission_classes = (IsAuthenticatedAndActive,)

    def filter_queryset(self, queryset):
        qs = super().filter_queryset(queryset)
        qs.do_read(self.request.user)
        return qs


class MessageCreateView(generics.CreateAPIView):
    serializer_class = MessageCreateSerializer
    permission_classes = (IsAuthenticatedAndActive,)

    def perform_create(self, serializer):
        creator = self.request.user
        message = serializer.save(creator=creator)
        message.do_read(creator)
        message.chat.save(update_fields=("updated_date",))


class MessageUpdateView(generics.UpdateAPIView):
    serializer_class = MessageUpdateSerializer
    queryset = Message.objects.filter(is_deleted=False).prefetch_related("attachments")
    permission_classes = (IsNotGuest,)

    def check_object_permissions(self, request, obj):
        if self.request.user.role == User.ROLE_MODERATOR:
            return
        if obj.creator_id != self.request.user.pk:
            raise PermissionDenied

    def perform_update(self, serializer):
        message = serializer.save()
        message.do_read(self.request.user)


class MessageDeleteView(generics.UpdateAPIView):
    serializer_class = MessageDeleteSerializer
    queryset = Message.objects.filter(is_deleted=False).prefetch_related("attachments")
    permission_classes = (IsNotGuest,)

    def check_object_permissions(self, request, obj):
        if self.request.user.role == User.ROLE_MODERATOR:
            return
        if obj.creator_id != self.request.user.pk:
            raise PermissionDenied

    def perform_update(self, serializer):
        serializer.save(is_deleted=True)
