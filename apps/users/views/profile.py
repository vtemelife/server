from apps.generic.permissions import IsAuthenticatedAndActive, IsReal
from apps.users.models import User
from apps.users.serializers.profile import (
    ProfileChangePasswordSerializer,
    ProfileDeleteSerializer,
    ProfileGiveRealStatusSerializer,
    ProfileSerializer,
    ProfileUpdateSerializer,
)
from django.core.exceptions import PermissionDenied
from rest_framework import generics


class ProfileView(generics.RetrieveAPIView):
    serializer_class = ProfileSerializer
    queryset = User.objects.with_online().filter(is_active=True).select_related("approver").prefetch_related("friends")
    permission_classes = (IsAuthenticatedAndActive,)
    lookup_field = "slug"

    def get_serializer(self, instance, *args, **kwargs):
        if instance.is_deleted:
            self.serializer_class = ProfileDeleteSerializer
        return super().get_serializer(instance, *args, **kwargs)


class ProfileUpdateView(generics.UpdateAPIView):
    serializer_class = ProfileUpdateSerializer
    queryset = User.objects.filter(is_active=True, is_deleted=False)
    permission_classes = (IsAuthenticatedAndActive,)
    lookup_field = "slug"

    def check_object_permissions(self, request, obj):
        if obj.pk != request.user.pk:
            raise PermissionDenied


class ProfileChangePasswordView(generics.UpdateAPIView):
    serializer_class = ProfileChangePasswordSerializer
    queryset = User.objects.filter(is_active=True, is_deleted=False)
    permission_classes = (IsAuthenticatedAndActive,)
    lookup_field = "slug"

    def check_object_permissions(self, request, obj):
        if obj.pk != request.user.pk:
            raise PermissionDenied


class ProfileDeleteView(generics.UpdateAPIView):
    serializer_class = ProfileDeleteSerializer
    queryset = User.objects.filter(is_active=True, is_deleted=False)
    permission_classes = (IsAuthenticatedAndActive,)
    lookup_field = "slug"

    def check_object_permissions(self, request, obj):
        if obj.pk != request.user.pk:
            raise PermissionDenied

    def perform_update(self, serializer):
        return serializer.save(is_deleted=True, is_active=False)


class ProfileGiveRealStatusView(generics.UpdateAPIView):
    serializer_class = ProfileGiveRealStatusSerializer
    queryset = User.objects.filter(is_active=True, is_deleted=False)
    permission_classes = (IsReal,)
    lookup_field = "slug"

    def check_object_permissions(self, request, obj):
        if obj.pk == request.user.pk:
            raise PermissionDenied
        if obj.is_real:
            raise PermissionDenied

    def perform_update(self, serializer):
        return serializer.save(approver=self.request.user)
