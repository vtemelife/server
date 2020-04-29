from apps.generic.permissions import IsNotGuest
from apps.users.models import User
from django.core.exceptions import PermissionDenied
from rest_framework import generics

from .filtersets import GroupFilterSet
from .models import Group
from .serializers import (
    GroupCreateUpdateSerializer,
    GroupDeleteSerializer,
    GroupLeaveSerializer,
    GroupListSerializer,
    GroupRetrieveSerializer,
)


class GroupListView(generics.ListAPIView):
    serializer_class = GroupListSerializer
    queryset = (
        Group.objects.filter(is_deleted=False)
        .select_related("creator")
        .prefetch_related("moderators", "users", "requests")
    )
    permission_classes = (IsNotGuest,)
    filterset_class = GroupFilterSet
    search_fields = ("name", "description")


class GroupRetrieveView(generics.RetrieveAPIView):
    serializer_class = GroupRetrieveSerializer
    queryset = (
        Group.objects.filter(is_deleted=False)
        .select_related("creator")
        .prefetch_related("moderators", "users", "requests")
    )
    permission_classes = (IsNotGuest,)
    lookup_field = "slug"


class GroupCreateView(generics.CreateAPIView):
    serializer_class = GroupCreateUpdateSerializer
    queryset = Group.objects.filter(is_deleted=False)
    permission_classes = (IsNotGuest,)

    def perform_create(self, serializer):
        instance = serializer.save(creator=self.request.user)
        instance.moderators.add(self.request.user)
        instance.users.add(self.request.user)


class GroupUpdateView(generics.UpdateAPIView):
    serializer_class = GroupCreateUpdateSerializer
    queryset = Group.objects.filter(is_deleted=False).prefetch_related("moderators")
    permission_classes = (IsNotGuest,)
    lookup_field = "slug"

    def check_object_permissions(self, request, obj):
        if self.request.user.role == User.ROLE_MODERATOR:
            return
        if not obj.moderators.filter(pk=request.user.pk).exists():
            raise PermissionDenied


class GroupDeleteView(generics.UpdateAPIView):
    serializer_class = GroupDeleteSerializer
    queryset = Group.objects.filter(is_deleted=False).prefetch_related("moderators")
    permission_classes = (IsNotGuest,)
    lookup_field = "slug"

    def check_object_permissions(self, request, obj):
        if self.request.user.role == User.ROLE_MODERATOR:
            return
        if not obj.moderators.filter(pk=request.user.pk).exists():
            raise PermissionDenied

    def perform_update(self, serializer):
        return serializer.save(is_deleted=True)


class GroupLeaveView(generics.UpdateAPIView):
    serializer_class = GroupLeaveSerializer
    queryset = Group.objects.filter(is_deleted=False).prefetch_related("users")
    permission_classes = (IsNotGuest,)
    lookup_field = "slug"

    def check_object_permissions(self, request, obj):
        if not obj.users.filter(pk=request.user.pk).exists():
            raise PermissionDenied

    def perform_update(self, serializer):
        instance = serializer.instance
        instance.users.remove(self.request.user)
        instance.moderators.remove(self.request.user)
        return instance
