from django.utils import timezone
from django_filters import filters, filterset

from .models import Party


class PastFilter(filters.CharFilter):
    def filter(self, qs, value):
        if value == "true":
            qs = qs.filter(start_date__lt=timezone.now()).order_by("-start_date")
        elif value == "false":
            qs = qs.filter(start_date__gte=timezone.now()).order_by("start_date")
        else:
            qs = qs.order_by("-start_date")
        return qs


class PartyParticipantFilter(filters.CharFilter):
    def filter(self, qs, value):
        if value == "true":
            qs = qs.filter(partyuser__user=self.parent.request.user)
        return qs


class PartyFilterSet(filterset.FilterSet):
    hash_tag = filters.CharFilter(field_name="hash_tags", lookup_expr="icontains")
    is_participant = PartyParticipantFilter()
    is_past = PastFilter()

    class Meta:
        model = Party
        fields = ("club", "city__country", "city__region", "city", "theme", "hash_tag", "is_participant", "is_past")
