from django.urls import path

from .views import (
    ChatBanUserView,
    ChatBlockUserView,
    ChatConversationCreateView,
    ChatCreateView,
    ChatDeleteView,
    ChatLeaveView,
    ChatListView,
    ChatMessagesReadAll,
    ChatReadAll,
    ChatRetrieveView,
    ChatUpdateView,
    ChatWithModeratorsCreateView,
    MessageCreateView,
    MessageDeleteView,
    MessageListView,
    MessageUpdateView,
)

app_name = "apps.chat"

urlpatterns = [
    path("list/", ChatListView.as_view(), name="chat-list"),
    path("conversation/create/", ChatConversationCreateView.as_view(), name="chat-conversation-create"),
    path("chat/create/", ChatCreateView.as_view(), name="chat-create"),
    path("chat_with_moderators/create/", ChatWithModeratorsCreateView.as_view(), name="chat-with-moderators-create"),
    path("<uuid:pk>/detail/", ChatRetrieveView.as_view(), name="chat-retrieve"),
    path("<uuid:pk>/update/", ChatUpdateView.as_view(), name="chat-update"),
    path("<uuid:pk>/delete/", ChatDeleteView.as_view(), name="chat-delete"),
    path("<uuid:pk>/leave/", ChatLeaveView.as_view(), name="chat-leave"),
    path("<uuid:pk>/ban/user/", ChatBanUserView.as_view(), name="chat-ban-user"),
    path("<uuid:pk>/block/user/", ChatBlockUserView.as_view(), name="chat-block-user"),
    path("<uuid:pk>/read-all/", ChatMessagesReadAll.as_view(), name="chat-messages-read-all"),
    path("read-all/", ChatReadAll.as_view(), name="chat-read-all"),
    path("message/list/", MessageListView.as_view(), name="message-list"),
    path("message/create/", MessageCreateView.as_view(), name="message-create"),
    path("message/<uuid:pk>/update/", MessageUpdateView.as_view(), name="message-update"),
    path("message/<uuid:pk>/delete/", MessageDeleteView.as_view(), name="message-delete"),
]
