from django.db.models import Count
from rest_framework import generics

from apps.generic.permissions import IsAuthenticatedAndActive
from apps.users.filtersets.friends import FriendListFilterSet, FriendSearchFilterSet
from apps.users.models import User
from apps.users.serializers.friends import FriendDeleteSerializer, FriendListItemSerializer, FriendSearchSerializer


class FriendSearchView(generics.ListAPIView):
    serializer_class = FriendSearchSerializer
    queryset = User.objects.with_online().filter(is_active=True, is_deleted=False).exclude(role=User.ROLE_GUEST)
    permission_classes = (IsAuthenticatedAndActive,)
    filterset_class = FriendSearchFilterSet
    search_fields = ("slug", "email")

    def get_queryset(self):
        qs = super().get_queryset()
        user = self.request.user
        qs = qs.exclude(pk=self.request.user.pk)
        qs = qs.exclude(friends=self.request.user)
        qs = qs.exclude(pk__in=user.black_list.all().values_list("pk", flat=True))
        qs = qs.exclude(black_list__pk=user.pk)
        qs = qs.annotate(last_seen_count=Count("user_online__last_seen"))
        return qs.distinct()

    def filter_queryset(self, queryset):
        qs = super().filter_queryset(queryset)
        return qs.order_by("-is_real", "-last_seen_count", "-user_online__last_seen")


class FriendListView(generics.ListAPIView):
    serializer_class = FriendListItemSerializer
    permission_classes = (IsAuthenticatedAndActive,)
    queryset = User.objects.with_online().filter(is_active=True, is_deleted=False)
    filterset_class = FriendListFilterSet
    search_fields = ("slug", "email")

    def get_queryset(self):
        qs = super().get_queryset()
        user = self.request.user
        qs = qs.exclude(pk=self.request.user.pk)
        qs = qs.filter(friends=self.request.user)
        qs = qs.exclude(pk__in=user.black_list.all().values_list("pk", flat=True))
        qs = qs.exclude(black_list__pk=user.pk)
        qs = qs.annotate(last_seen_count=Count("user_online__last_seen"))
        return qs.distinct()

    def filter_queryset(self, queryset):
        qs = super().filter_queryset(queryset)
        return qs.order_by("-is_real", "-last_seen_count", "-user_online__last_seen")


class FriendDeleteView(generics.UpdateAPIView):
    permission_classes = (IsAuthenticatedAndActive,)
    serializer_class = FriendDeleteSerializer
    queryset = User.objects.filter(is_active=True, is_deleted=False)
    lookup_field = "slug"

    def perform_update(self, serializer):
        instance = serializer.instance
        self.request.user.friends.remove(instance)
        instance.friends.remove(self.request.user)
        return instance
