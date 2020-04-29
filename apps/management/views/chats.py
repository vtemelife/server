from apps.chat.filtersets import ChatFilterSet
from apps.chat.views import ChatListView
from apps.generic.permissions import IsModerator


class ChatWithModeratorsAndDevelopersListView(ChatListView):
    permission_classes = (IsModerator,)
    filterset_class = ChatFilterSet
    is_moderator = True
