from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import PermissionDenied
from django.db.models import F
from rest_framework import generics

from apps.generic.choices import AccessChoices
from apps.generic.permissions import IsAuthenticatedAndActive
from apps.users.models import User

from .filtersets import MediaFilterSet, MediaFolderFilterSet
from .models import Media, MediaFolder
from .serializers import (
    MediaCreateSerializer,
    MediaDeleteSerializer,
    MediaFolderCreateSerializer,
    MediaFolderDeleteSerializer,
    MediaFolderItemSerializer,
    MediaFolderSerializer,
    MediaFolderUpdateSerializer,
    MediaItemSerializer,
    MediaLikeSerializer,
    MediaSerializer,
    MediaToModerateMediaSerializer,
    MediaUpdateSerializer,
)


class MediaFolderListView(generics.ListAPIView):
    serializer_class = MediaFolderItemSerializer
    queryset = MediaFolder.objects.filter(is_deleted=False)
    permission_classes = (IsAuthenticatedAndActive,)
    filterset_class = MediaFolderFilterSet
    search_fields = ("name",)


class MediaFolderRetrieveView(generics.RetrieveAPIView):
    serializer_class = MediaFolderSerializer
    queryset = MediaFolder.objects.filter(is_deleted=False).prefetch_related("creator__friends")
    permission_classes = (IsAuthenticatedAndActive,)

    def check_object_permissions(self, request, obj):
        user = request.user
        if user.role == User.ROLE_MODERATOR:
            return
        if obj.show_media == AccessChoices.ACCESS_NO_USERS and obj.creator_id != user.pk:
            raise PermissionDenied
        if (
            obj.show_media == AccessChoices.ACCESS_ONLY_FRIENDS
            and obj.creator_id != user.pk
            and not obj.creator.friends.filter(pk=user.pk).exists()
        ):
            raise PermissionDenied


class MediaFolderCreateView(generics.CreateAPIView):
    serializer_class = MediaFolderCreateSerializer
    queryset = MediaFolder.objects.filter(is_deleted=False)
    permission_classes = (IsAuthenticatedAndActive,)

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)


class MediaFolderUpdateView(generics.UpdateAPIView):
    serializer_class = MediaFolderUpdateSerializer
    queryset = MediaFolder.objects.filter(is_deleted=False)
    permission_classes = (IsAuthenticatedAndActive,)

    def check_object_permissions(self, request, obj):
        if self.request.user.role == User.ROLE_MODERATOR:
            return
        if obj.creator_id != request.user.pk:
            raise PermissionDenied


class MediaFolderDeleteView(generics.UpdateAPIView):
    serializer_class = MediaFolderDeleteSerializer
    queryset = MediaFolder.objects.filter(is_deleted=False)
    permission_classes = (IsAuthenticatedAndActive,)

    def check_object_permissions(self, request, obj):
        if obj.creator_id != request.user.pk:
            raise PermissionDenied

    def perform_update(self, serializer):
        return serializer.save(is_deleted=True)


class MediaListView(generics.ListAPIView):
    serializer_class = MediaItemSerializer
    queryset = Media.objects.filter(is_deleted=False).order_by("-updated_date")
    permission_classes = (IsAuthenticatedAndActive,)
    filterset_class = MediaFilterSet
    search_fields = ("title", "description", "creator__slug", "creator__name")


class MediaRetrieveView(generics.RetrieveAPIView):
    serializer_class = MediaSerializer
    queryset = Media.objects.filter(is_deleted=False).prefetch_related("creator__friends")
    permission_classes = (IsAuthenticatedAndActive,)

    def check_object_permissions(self, request, obj):
        if obj.status == Media.STATUS_APPROVED:
            return
        media_folder_ct = ContentType.objects.get_for_model(MediaFolder)
        if obj.content_type != media_folder_ct:
            return
        user = request.user
        if user.role == User.ROLE_MODERATOR:
            return
        media_folder = obj.content_object
        if media_folder.show_media == AccessChoices.ACCESS_NO_USERS and media_folder.creator_id != user.pk:
            raise PermissionDenied
        if (
            media_folder.show_media == AccessChoices.ACCESS_ONLY_FRIENDS
            and media_folder.creator_id != user.pk
            and not media_folder.creator.friends.filter(pk=user.pk).exists()
        ):
            raise PermissionDenied

    def get_object(self, *args, **kwargs):
        obj = super().get_object(*args, **kwargs)
        obj.views += 1
        Media.objects.filter(pk=obj.pk).update(views=F("views") + 1)
        return obj


class MediaCreateView(generics.CreateAPIView):
    serializer_class = MediaCreateSerializer
    queryset = Media.objects.filter(is_deleted=False)
    permission_classes = (IsAuthenticatedAndActive,)

    def check_object_permissions(self, request, validated_data):
        content_type = validated_data.get("content_type")
        object_id = validated_data.get("object_id")
        if not content_type or not object_id:
            return
        media_folder_ct = ContentType.objects.get_for_model(MediaFolder)
        if content_type != media_folder_ct:
            return
        media_folder = MediaFolder.objects.filter(pk=object_id).first()
        if not media_folder:
            return
        user = request.user
        if media_folder.creator_id != user.pk:
            raise PermissionDenied

    def perform_create(self, serializer):
        self.check_object_permissions(self.request, serializer.validated_data)
        serializer.save(creator=self.request.user)


class MediaUpdateView(generics.UpdateAPIView):
    serializer_class = MediaUpdateSerializer
    queryset = Media.objects.filter(is_deleted=False)
    permission_classes = (IsAuthenticatedAndActive,)

    def check_object_permissions(self, request, obj):
        if self.request.user.role == User.ROLE_MODERATOR:
            return
        if obj.creator_id != request.user.pk:
            raise PermissionDenied


class MediaDeleteView(generics.UpdateAPIView):
    serializer_class = MediaDeleteSerializer
    queryset = Media.objects.filter(is_deleted=False)
    permission_classes = (IsAuthenticatedAndActive,)

    def check_object_permissions(self, request, obj):
        if obj.creator_id != request.user.pk:
            raise PermissionDenied

    def perform_update(self, serializer):
        return serializer.save(is_deleted=True)


class MediaLikeView(generics.UpdateAPIView):
    serializer_class = MediaLikeSerializer
    queryset = Media.objects.filter(is_deleted=False)
    permission_classes = (IsAuthenticatedAndActive,)

    def perform_update(self, serializer):
        instance = serializer.instance
        if instance.likes.filter(pk=self.request.user.pk):
            instance.likes.remove(self.request.user)
        else:
            instance.likes.add(self.request.user)
        return instance


class MediaToModerateMediaView(generics.UpdateAPIView):
    serializer_class = MediaToModerateMediaSerializer
    queryset = Media.objects.filter(is_deleted=False, status__isnull=True)
    permission_classes = (IsAuthenticatedAndActive,)

    def perform_update(self, serializer):
        return serializer.save(status=Media.STATUS_WAITING_MODERATION)
