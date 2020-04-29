from django.core.exceptions import PermissionDenied
from django.db.models import F
from rest_framework import generics

from apps.generic.permissions import IsAuthenticatedAndActive
from apps.users.models import User

from .filtersets import PostFilterSet
from .models import Post
from .serializers import (
    PostCreateUpdateSerializer,
    PostDeleteSerializer,
    PostItemSerializer,
    PostLikeSerializer,
    PostSerializer,
    PostToModerateSerializer,
    WhisperToModerateSerializer,
)


class PostListView(generics.ListAPIView):
    serializer_class = PostItemSerializer
    queryset = Post.objects.filter(is_deleted=False).order_by("-updated_date")
    permission_classes = (IsAuthenticatedAndActive,)
    filterset_class = PostFilterSet
    search_fields = ("title", "description")


class PostRetrieveView(generics.RetrieveAPIView):
    serializer_class = PostSerializer
    queryset = Post.objects.filter(is_deleted=False)
    permission_classes = (IsAuthenticatedAndActive,)
    lookup_field = "slug"

    def get_object(self, *args, **kwargs):
        obj = super().get_object(*args, **kwargs)
        obj.views += 1
        Post.objects.filter(pk=obj.pk).update(views=F("views") + 1)
        return obj


class PostCreateView(generics.CreateAPIView):
    serializer_class = PostCreateUpdateSerializer
    queryset = Post.objects.filter(is_deleted=False)
    permission_classes = (IsAuthenticatedAndActive,)

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)


class PostUpdateView(generics.UpdateAPIView):
    serializer_class = PostCreateUpdateSerializer
    queryset = Post.objects.filter(is_deleted=False)
    permission_classes = (IsAuthenticatedAndActive,)
    lookup_field = "slug"

    def check_object_permissions(self, request, obj):
        if self.request.user.role == User.ROLE_MODERATOR:
            return
        if obj.creator_id != request.user.pk:
            raise PermissionDenied


class PostDeleteView(generics.UpdateAPIView):
    serializer_class = PostDeleteSerializer
    queryset = Post.objects.filter(is_deleted=False)
    permission_classes = (IsAuthenticatedAndActive,)
    lookup_field = "slug"

    def check_object_permissions(self, request, obj):
        if obj.creator_id != request.user.pk:
            raise PermissionDenied

    def perform_update(self, serializer):
        return serializer.save(is_deleted=True)


class PostLikeView(generics.UpdateAPIView):
    serializer_class = PostLikeSerializer
    queryset = Post.objects.filter(is_deleted=False)
    permission_classes = (IsAuthenticatedAndActive,)
    lookup_field = "slug"

    def perform_update(self, serializer):
        instance = serializer.instance
        if instance.likes.filter(pk=self.request.user.pk):
            instance.likes.remove(self.request.user)
        else:
            instance.likes.add(self.request.user)
        return instance


class PostToModerateView(generics.UpdateAPIView):
    serializer_class = PostToModerateSerializer
    queryset = Post.objects.filter(is_deleted=False, status__isnull=True)
    permission_classes = (IsAuthenticatedAndActive,)
    lookup_field = "slug"

    def check_object_permissions(self, request, obj):
        if obj.creator_id != request.user.pk:
            raise PermissionDenied

    def perform_update(self, serializer):
        return serializer.save(is_whisper=False, status=Post.STATUS_WAITING_MODERATION)


class WhisperToModerateView(generics.UpdateAPIView):
    serializer_class = WhisperToModerateSerializer
    queryset = Post.objects.filter(is_deleted=False, status__isnull=True)
    permission_classes = (IsAuthenticatedAndActive,)
    lookup_field = "slug"

    def check_object_permissions(self, request, obj):
        if obj.creator_id != request.user.pk:
            raise PermissionDenied

    def perform_update(self, serializer):
        return serializer.save(is_whisper=True, status=Post.STATUS_WAITING_MODERATION)
