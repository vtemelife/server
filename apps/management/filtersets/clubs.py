from apps.clubs.models import Club
from apps.generic.filtersets import BoolFilter
from django_filters import filterset


class ClubFilterSet(filterset.FilterSet):
    is_ban = BoolFilter()

    class Meta:
        model = Club
        fields = ("name", "status", "is_ban")
