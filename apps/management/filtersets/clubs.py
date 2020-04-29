from django_filters import filterset

from apps.clubs.models import Club
from apps.generic.filtersets import BoolFilter


class ClubFilterSet(filterset.FilterSet):
    is_ban = BoolFilter()

    class Meta:
        model = Club
        fields = ("name", "status", "is_ban")
