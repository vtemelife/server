from apps.clubs.models import Club
from apps.generic.permissions import IsAuthenticatedAndActive
from apps.groups.models import Group
from apps.users.models import User
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import PermissionDenied
from rest_framework import generics

from .filtersets import MembershipRequestFilterSet
from .models import MembershipRequest
from .serializers import (
    MembershipRequestCreateSerializer,
    MembershipRequestDeleteSerializer,
    MembershipRequestListItemSerializer,
    MembershipRequestUpdateSerializer,
)


class MembershipRequestListView(generics.ListAPIView):
    serializer_class = MembershipRequestListItemSerializer
    permission_classes = (IsAuthenticatedAndActive,)
    filterset_class = MembershipRequestFilterSet
    queryset = MembershipRequest.objects.filter(is_deleted=False).select_related("user")
    search_fields = ("user__slug", "user__name")


class MembershipRequestCreateView(generics.CreateAPIView):
    permission_classes = (IsAuthenticatedAndActive,)
    serializer_class = MembershipRequestCreateSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user, status=MembershipRequest.STATUS_WAITING_MODERATION)


class MembershipRequestUpdateView(generics.UpdateAPIView):
    permission_classes = (IsAuthenticatedAndActive,)
    serializer_class = MembershipRequestUpdateSerializer
    queryset = MembershipRequest.objects.filter(is_deleted=False)

    def check_object_permissions(self, request, obj):
        ct_user = ContentType.objects.get_for_model(User)
        ct_group = ContentType.objects.get_for_model(Group)
        ct_club = ContentType.objects.get_for_model(Club)
        if obj.content_type == ct_user:
            if obj.content_object.pk != request.user.pk:
                raise PermissionDenied
        if obj.content_type == ct_group:
            if self.request.user.role == User.ROLE_MODERATOR:
                return
            if not obj.content_object.moderators.filter(pk=request.user.pk).exists():
                raise PermissionDenied
        if obj.content_type == ct_club:
            if self.request.user.role == User.ROLE_MODERATOR:
                return
            if not obj.content_object.moderators.filter(pk=request.user.pk).exists():
                raise PermissionDenied


class MembershipRequestDeleteView(generics.UpdateAPIView):
    permission_classes = (IsAuthenticatedAndActive,)
    serializer_class = MembershipRequestDeleteSerializer
    queryset = MembershipRequest.objects.filter(is_deleted=False)

    def check_object_permissions(self, request, obj):
        if self.request.user.role == User.ROLE_MODERATOR:
            return
        if obj.user_id != request.user.pk:
            raise PermissionDenied

    def perform_update(self, serializer):
        return serializer.save(is_deleted=True)
