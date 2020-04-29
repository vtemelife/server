from apps.generic.filtersets import ParticipantFilter
from django_filters import filterset

from .models import Group


class GroupFilterSet(filterset.FilterSet):
    is_participant = ParticipantFilter()

    class Meta:
        model = Group
        fields = ("relationship_theme", "group_type", "is_participant")
