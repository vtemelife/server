from rest_framework import generics

from apps.generic.permissions import IsModerator
from apps.management.filtersets.posts import PostFilterSet
from apps.management.serializers.posts import (
    PostApproveSerializer,
    PostDeclineSerializer,
    PostListSerializer,
    PostToggleBanSerializer,
)
from apps.posts.models import Post


class PostListView(generics.ListAPIView):
    serializer_class = PostListSerializer
    queryset = Post.objects.filter(is_deleted=False).select_related("creator").order_by("-created_date")
    permission_classes = (IsModerator,)
    filterset_class = PostFilterSet
    search_fields = ("title", "slug")


class PostToggleBanView(generics.UpdateAPIView):
    serializer_class = PostToggleBanSerializer
    queryset = Post.objects.filter(is_deleted=False)
    permission_classes = (IsModerator,)

    def perform_update(self, serializer):
        return serializer.save(is_ban=not serializer.instance.is_ban)


class PostApproveView(generics.UpdateAPIView):
    serializer_class = PostApproveSerializer
    queryset = Post.objects.filter(is_deleted=False)
    permission_classes = (IsModerator,)

    def perform_update(self, serializer):
        return serializer.save(status=Post.STATUS_APPROVED)


class PostDeclineView(generics.UpdateAPIView):
    serializer_class = PostDeclineSerializer
    queryset = Post.objects.filter(is_deleted=False)
    permission_classes = (IsModerator,)

    def perform_update(self, serializer):
        return serializer.save(status=Post.STATUS_DECLINED)
