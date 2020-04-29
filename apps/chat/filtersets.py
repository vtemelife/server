from django_filters import filters, filterset

from .models import Chat, Message


class UnreadFilter(filters.CharFilter):
    def filter(self, qs, value):
        if value == "true":
            return qs.unread(self.parent.request.user)
        return qs


class ChatFilterSet(filterset.FilterSet):
    is_unread = UnreadFilter()

    class Meta:
        model = Chat
        fields = ("chat_type", "is_unread")


class MessageFilterSet(filterset.FilterSet):
    class Meta:
        model = Message
        fields = ("chat",)
