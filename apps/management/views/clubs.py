from rest_framework import generics

from apps.clubs.models import Club
from apps.generic.permissions import IsModerator
from apps.management.filtersets.clubs import ClubFilterSet
from apps.management.serializers.clubs import (
    ClubApproveSerializer,
    ClubDeclineSerializer,
    ClubListSerializer,
    ClubToggleBanSerializer,
)


class ClubListView(generics.ListAPIView):
    serializer_class = ClubListSerializer
    queryset = Club.objects.filter(is_deleted=False).select_related("creator", "city").order_by("-created_date")
    permission_classes = (IsModerator,)
    filterset_class = ClubFilterSet
    search_fields = ("name", "id")


class ClubToggleBanView(generics.UpdateAPIView):
    serializer_class = ClubToggleBanSerializer
    queryset = Club.objects.filter(is_deleted=False)
    permission_classes = (IsModerator,)

    def perform_update(self, serializer):
        return serializer.save(is_ban=not serializer.instance.is_ban)


class ClubApproveView(generics.UpdateAPIView):
    serializer_class = ClubApproveSerializer
    queryset = Club.objects.filter(is_deleted=False)
    permission_classes = (IsModerator,)

    def perform_update(self, serializer):
        return serializer.save(status=Club.STATUS_APPROVED)


class ClubDeclineView(generics.UpdateAPIView):
    serializer_class = ClubDeclineSerializer
    queryset = Club.objects.filter(is_deleted=False)
    permission_classes = (IsModerator,)

    def perform_update(self, serializer):
        return serializer.save(status=Club.STATUS_DECLINED)
