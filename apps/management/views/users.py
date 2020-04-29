from rest_framework import generics

from apps.generic.permissions import IsModerator
from apps.management.filtersets.users import UserFilterSet
from apps.management.serializers.users import (
    UserListSerializer,
    UserSetMemberSerializer,
    UserSetRealSerializer,
    UserToggleBanSerializer,
)
from apps.users.models import User


class UserListView(generics.ListAPIView):
    serializer_class = UserListSerializer
    queryset = User.objects.filter(is_deleted=False, is_active=True).order_by("-created_date")
    permission_classes = (IsModerator,)
    filterset_class = UserFilterSet
    search_fields = ("slug", "name", "email", "slug", "id")


class UserToggleBanView(generics.UpdateAPIView):
    serializer_class = UserToggleBanSerializer
    queryset = User.objects.filter(is_deleted=False, is_active=True)
    permission_classes = (IsModerator,)

    def perform_update(self, serializer):
        return serializer.save(is_ban=not serializer.instance.is_ban)


class UserSetMemberView(generics.UpdateAPIView):
    serializer_class = UserSetMemberSerializer
    queryset = User.objects.filter(is_deleted=False, is_active=True, role=User.ROLE_GUEST)
    permission_classes = (IsModerator,)

    def perform_update(self, serializer):
        return serializer.save(role=User.ROLE_MEMBER)


class UserSetRealView(generics.UpdateAPIView):
    serializer_class = UserSetRealSerializer
    queryset = User.objects.filter(is_deleted=False, is_active=True, is_real=False)
    permission_classes = (IsModerator,)

    def perform_update(self, serializer):
        return serializer.save(is_real=True)
