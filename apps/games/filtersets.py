from django_filters import filters, filterset

from apps.generic.filtersets import ParticipantFilter

from .models import Game


class GameFilterSet(filterset.FilterSet):
    hash_tag = filters.CharFilter(field_name="hash_tags", lookup_expr="icontains")
    is_participant = ParticipantFilter()

    class Meta:
        model = Game
        fields = ("status", "hash_tag", "is_participant")
