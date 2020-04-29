from apps.generic.permissions import IsNotGuest
from apps.users.models import User
from django.core.exceptions import PermissionDenied
from django.db.models import Q
from rest_framework import generics

from .filtersets import ClubFilterSet
from .models import Club
from .serializers import (
    ClubCreateUpdateSerializer,
    ClubDeleteSerializer,
    ClubLeaveSerializer,
    ClubListSerializer,
    ClubRetrieveSerializer,
)


class ClubListView(generics.ListAPIView):
    serializer_class = ClubListSerializer
    queryset = (
        Club.objects.filter(is_deleted=False)
        .select_related("city", "creator")
        .prefetch_related("moderators", "users", "requests")
    )
    permission_classes = (IsNotGuest,)
    filterset_class = ClubFilterSet
    search_fields = ("name", "description")

    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.filter(Q(moderators=self.request.user) | Q(status=Club.STATUS_APPROVED))
        return qs.distinct()


class ClubRetrieveView(generics.RetrieveAPIView):
    serializer_class = ClubRetrieveSerializer
    queryset = (
        Club.objects.filter(is_deleted=False)
        .select_related("city", "creator")
        .prefetch_related("moderators", "users", "requests")
    )
    permission_classes = (IsNotGuest,)
    lookup_field = "slug"

    def check_object_permissions(self, request, obj):
        if request.user.role == User.ROLE_MODERATOR:
            return
        if not obj.moderators.filter(pk=request.user.pk).exists() and obj.status != Club.STATUS_APPROVED:
            raise PermissionDenied


class ClubCreateView(generics.CreateAPIView):
    serializer_class = ClubCreateUpdateSerializer
    queryset = Club.objects.filter(is_deleted=False)
    permission_classes = (IsNotGuest,)

    def perform_create(self, serializer):
        instance = serializer.save(creator=self.request.user, status=Club.STATUS_WAITING_MODERATION)
        instance.moderators.add(self.request.user)
        instance.users.add(self.request.user)


class ClubUpdateView(generics.UpdateAPIView):
    serializer_class = ClubCreateUpdateSerializer
    queryset = Club.objects.filter(is_deleted=False).prefetch_related("moderators")
    permission_classes = (IsNotGuest,)
    lookup_field = "slug"

    def check_object_permissions(self, request, obj):
        if self.request.user.role == User.ROLE_MODERATOR:
            return
        if not obj.moderators.filter(pk=request.user.pk).exists():
            raise PermissionDenied


class ClubDeleteView(generics.UpdateAPIView):
    serializer_class = ClubDeleteSerializer
    queryset = Club.objects.filter(is_deleted=False).prefetch_related("moderators")
    permission_classes = (IsNotGuest,)
    lookup_field = "slug"

    def check_object_permissions(self, request, obj):
        if self.request.user.role == User.ROLE_MODERATOR:
            return
        if not obj.moderators.filter(pk=request.user.pk).exists():
            raise PermissionDenied

    def perform_update(self, serializer):
        return serializer.save(is_deleted=True)


class ClubLeaveView(generics.UpdateAPIView):
    serializer_class = ClubLeaveSerializer
    queryset = Club.objects.filter(is_deleted=False).prefetch_related("users")
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
