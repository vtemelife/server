from apps.chat.filtersets import UnreadFilter
from apps.chat.models import Chat
from django_filters import filterset


class ChatFilterSet(filterset.FilterSet):
    is_unread = UnreadFilter()

    class Meta:
        model = Chat
        fields = ("chat_type", "is_unread")
