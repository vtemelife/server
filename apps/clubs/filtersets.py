from apps.generic.filtersets import ParticipantFilter
from django_filters import filterset

from .models import Club


class ClubFilterSet(filterset.FilterSet):
    is_participant = ParticipantFilter()

    class Meta:
        model = Club
        fields = ("city__country", "city__region", "city", "relationship_theme", "club_type", "is_participant")
