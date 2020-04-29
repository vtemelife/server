from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404
from rest_framework import generics

from apps.generic.pagination import ReverseLimitOffsetPagination
from apps.generic.permissions import IsAuthenticatedAndActive
from apps.posts.models import Post
from apps.users.models import User

from .filtersets import CommentFilterSet
from .models import Comment
from .serializers import (
    CommentCreateUpdateSerializer,
    CommentDeleteSerializer,
    CommentItemSerializer,
    CommentLikeSerializer,
    CommentWhisperSerializer,
)


class CommentListView(generics.ListAPIView):
    pagination_class = ReverseLimitOffsetPagination
    queryset = Comment.objects.filter(is_deleted=False).filter(parent__isnull=True)
    permission_classes = (IsAuthenticatedAndActive,)
    filterset_class = CommentFilterSet
    search_fields = ("comment",)

    def get_serializer_class(self):
        content_type = self.request.GET.get("content_type")
        object_id = self.request.GET.get("object_id")
        if object_id and content_type == "posts:post":
            post = get_object_or_404(Post, pk=object_id)
            if post.is_whisper:
                return CommentWhisperSerializer
        return CommentItemSerializer


class CommentCreateView(generics.CreateAPIView):
    serializer_class = CommentCreateUpdateSerializer
    queryset = Comment.objects.filter(is_deleted=False)
    permission_classes = (IsAuthenticatedAndActive,)

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)


class CommentUpdateView(generics.UpdateAPIView):
    serializer_class = CommentCreateUpdateSerializer
    queryset = Comment.objects.filter(is_deleted=False)
    permission_classes = (IsAuthenticatedAndActive,)

    def check_object_permissions(self, request, obj):
        if self.request.user.role == User.ROLE_MODERATOR:
            return
        if obj.creator_id != self.request.user.pk:
            raise PermissionDenied


class CommentDeleteView(generics.UpdateAPIView):
    serializer_class = CommentDeleteSerializer
    queryset = Comment.objects.filter(is_deleted=False)
    permission_classes = (IsAuthenticatedAndActive,)

    def check_object_permissions(self, request, obj):
        if self.request.user.role == User.ROLE_MODERATOR:
            return
        if obj.creator_id != self.request.user.pk:
            raise PermissionDenied

    def perform_update(self, serializer):
        serializer.save(is_deleted=True)


class CommentLikeView(generics.UpdateAPIView):
    serializer_class = CommentLikeSerializer
    queryset = Comment.objects.filter(is_deleted=False)
    permission_classes = (IsAuthenticatedAndActive,)

    def perform_update(self, serializer):
        instance = serializer.instance
        if instance.likes.filter(pk=self.request.user.pk):
            instance.likes.remove(self.request.user)
        else:
            instance.likes.add(self.request.user)
        return instance
