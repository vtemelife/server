from rest_framework import generics

from apps.generic.permissions import IsModerator
from apps.management.filtersets.media import MediaFilterSet
from apps.management.serializers.media import (
    MediaApproveSerializer,
    MediaDeclineSerializer,
    MediaListSerializer,
    MediaToggleBanSerializer,
)
from apps.media.models import Media


class MediaListView(generics.ListAPIView):
    serializer_class = MediaListSerializer
    queryset = Media.objects.filter(is_deleted=False).select_related("creator", "image").order_by("-created_date")
    permission_classes = (IsModerator,)
    filterset_class = MediaFilterSet
    search_fields = ("title", "id")


class MediaToggleBanView(generics.UpdateAPIView):
    serializer_class = MediaToggleBanSerializer
    queryset = Media.objects.filter(is_deleted=False)
    permission_classes = (IsModerator,)

    def perform_update(self, serializer):
        return serializer.save(is_ban=not serializer.instance.is_ban)


class MediaApproveView(generics.UpdateAPIView):
    serializer_class = MediaApproveSerializer
    queryset = Media.objects.filter(is_deleted=False)
    permission_classes = (IsModerator,)

    def perform_update(self, serializer):
        return serializer.save(status=Media.STATUS_APPROVED)


class MediaDeclineView(generics.UpdateAPIView):
    serializer_class = MediaDeclineSerializer
    queryset = Media.objects.filter(is_deleted=False)
    permission_classes = (IsModerator,)

    def perform_update(self, serializer):
        return serializer.save(status=Media.STATUS_DECLINED)
