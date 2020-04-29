from django_filters import filters, filterset

from .models import News


class UnreadFilter(filters.CharFilter):
    def filter(self, qs, value):
        if value == "true":
            return qs.unread(user=self.parent.request.user)
        return qs


class NewsFilterSet(filterset.FilterSet):
    is_unread = UnreadFilter()

    class Meta:
        model = News
        fields = ("news_type",)
