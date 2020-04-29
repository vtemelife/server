from django_filters import filters, filterset

from apps.news.models import News


class IsPublishFilter(filters.CharFilter):
    def filter(self, qs, value):
        if value == "true":
            return qs.published()
        if value == "false":
            return qs.not_published()
        return qs


class NewsFilterSet(filterset.FilterSet):
    is_publish = IsPublishFilter()

    class Meta:
        model = News
        fields = ("title", "is_publish")
