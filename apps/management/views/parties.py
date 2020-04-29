from apps.events.models import Party
from apps.generic.permissions import IsModerator
from apps.management.filtersets.parties import PartyFilterSet
from apps.management.serializers.parties import (
    PartyApproveSerializer,
    PartyDeclineSerializer,
    PartyListSerializer,
    PartyToggleBanSerializer,
)
from rest_framework import generics


class PartyListView(generics.ListAPIView):
    serializer_class = PartyListSerializer
    queryset = Party.objects.filter(is_deleted=False).select_related("city").order_by("-created_date")
    permission_classes = (IsModerator,)
    filterset_class = PartyFilterSet
    search_fields = ("name", "id")


class PartyToggleBanView(generics.UpdateAPIView):
    serializer_class = PartyToggleBanSerializer
    queryset = Party.objects.filter(is_deleted=False)
    permission_classes = (IsModerator,)

    def perform_update(self, serializer):
        return serializer.save(is_ban=not serializer.instance.is_ban)


class PartyApproveView(generics.UpdateAPIView):
    serializer_class = PartyApproveSerializer
    queryset = Party.objects.filter(is_deleted=False)
    permission_classes = (IsModerator,)

    def perform_update(self, serializer):
        return serializer.save(status=Party.STATUS_APPROVED)


class PartyDeclineView(generics.UpdateAPIView):
    serializer_class = PartyDeclineSerializer
    queryset = Party.objects.filter(is_deleted=False)
    permission_classes = (IsModerator,)

    def perform_update(self, serializer):
        return serializer.save(status=Party.STATUS_DECLINED)
