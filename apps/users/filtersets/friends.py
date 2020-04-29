from django_filters import filters, filterset

from apps.generic.filtersets import ArrayInFilter, BoolFilter, CharInFilter
from apps.users.models import User


class OnlineFilter(filters.CharFilter):
    def filter(self, qs, value):
        if value == "true":
            return qs.filter(online=True)
        return qs


class FriendSearchFilterSet(filterset.FilterSet):
    gender = CharInFilter(field_name="gender")
    relationship_formats = ArrayInFilter(field_name="relationship_formats")
    relationship_themes = ArrayInFilter(field_name="relationship_themes")
    is_online = OnlineFilter()
    is_real = BoolFilter()

    class Meta:
        model = User
        fields = (
            "city__region",
            "city__country",
            "city",
            "gender",
            "relationship_formats",
            "relationship_themes",
            "is_online",
            "is_real",
        )


class FriendListFilterSet(filterset.FilterSet):
    is_online = OnlineFilter()

    class Meta:
        model = User
        fields = ("is_online",)
