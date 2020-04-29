from django_filters import filterset

from apps.events.models import Party
from apps.generic.filtersets import BoolFilter


class PartyFilterSet(filterset.FilterSet):
    is_ban = BoolFilter()

    class Meta:
        model = Party
        fields = ("name", "status", "is_ban")
