from apps.events.models import Party
from apps.generic.filtersets import BoolFilter
from django_filters import filterset


class PartyFilterSet(filterset.FilterSet):
    is_ban = BoolFilter()

    class Meta:
        model = Party
        fields = ("name", "status", "is_ban")
