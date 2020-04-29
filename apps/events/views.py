from apps.clubs.models import Club
from apps.generic.permissions import IsAuthenticatedAndActive, IsNotGuest
from apps.users.models import User
from django.core.exceptions import PermissionDenied
from django.db.models import F, Q
from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework import generics
from rest_framework.response import Response

from .filtersets import PartyFilterSet
from .models import Party, PartyUser
from .serializers import (
    PartyApplySerializer,
    PartyCreateUpdateSerializer,
    PartyDeleteSerializer,
    PartyLikeSerializer,
    PartyListSerializer,
    PartyRetrieveSerializer,
)


class PartyListView(generics.ListAPIView):
    serializer_class = PartyListSerializer
    queryset = (
        Party.objects.filter(is_deleted=False)
        .select_related("club", "city", "club__creator")
        .prefetch_related("club__moderators")
    )
    permission_classes = (IsNotGuest,)
    filterset_class = PartyFilterSet
    search_fields = ("name", "short_description", "description")

    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.filter(Q(club__moderators=self.request.user) | Q(status=Party.STATUS_APPROVED))
        return qs.distinct()


class PartyRetrieveView(generics.RetrieveAPIView):
    serializer_class = PartyRetrieveSerializer
    queryset = (
        Party.objects.filter(is_deleted=False)
        .select_related("club", "city", "club__creator")
        .prefetch_related("club__moderators")
    )
    permission_classes = (IsNotGuest,)
    lookup_field = "slug"

    def get_object(self, *args, **kwargs):
        obj = super().get_object(*args, **kwargs)
        obj.views += 1
        Party.objects.filter(pk=obj.pk).update(views=F("views") + 1)
        return obj

    def check_object_permissions(self, request, obj):
        if request.user.role == User.ROLE_MODERATOR:
            return
        if not obj.club.moderators.filter(pk=request.user.pk).exists() and obj.status != Party.STATUS_APPROVED:
            raise PermissionDenied


class PartyCreateView(generics.CreateAPIView):
    serializer_class = PartyCreateUpdateSerializer
    queryset = Party.objects.filter(is_deleted=False)
    permission_classes = (IsNotGuest,)

    def perform_create(self, serializer):
        instance = serializer.save(status=Party.STATUS_WAITING_MODERATION)
        PartyUser.objects.get_or_create(user=self.request.user, party=instance)


class PartyUpdateView(generics.UpdateAPIView):
    serializer_class = PartyCreateUpdateSerializer
    queryset = Party.objects.filter(is_deleted=False).prefetch_related("club__moderators")
    permission_classes = (IsNotGuest,)
    lookup_field = "slug"

    def check_object_permissions(self, request, obj):
        if self.request.user.role == User.ROLE_MODERATOR:
            return
        if not obj.club.moderators.filter(pk=request.user.pk).exists():
            raise PermissionDenied


class PartyDeleteView(generics.UpdateAPIView):
    serializer_class = PartyDeleteSerializer
    queryset = Party.objects.filter(is_deleted=False).prefetch_related("club__moderators")
    permission_classes = (IsNotGuest,)
    lookup_field = "slug"

    def check_object_permissions(self, request, obj):
        if self.request.user.role == User.ROLE_MODERATOR:
            return
        if not obj.club.moderators.filter(pk=request.user.pk).exists():
            raise PermissionDenied

    def perform_update(self, serializer):
        return serializer.save(is_deleted=True)


class PartyLikeView(generics.UpdateAPIView):
    serializer_class = PartyLikeSerializer
    queryset = Party.objects.filter(is_deleted=False)
    permission_classes = (IsNotGuest,)
    lookup_field = "slug"

    def perform_update(self, serializer):
        instance = serializer.instance
        if instance.likes.filter(pk=self.request.user.pk):
            instance.likes.remove(self.request.user)
        else:
            instance.likes.add(self.request.user)
        return instance


class PartyApplyView(generics.GenericAPIView):
    serializer_class = PartyApplySerializer
    queryset = Party.objects.filter(is_deleted=False)
    permission_classes = (IsNotGuest,)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        status = serializer.validated_data["status"]
        party = get_object_or_404(self.queryset, slug=kwargs["slug"])
        if status == PartyUser.STATUS_UNKNOWN:
            PartyUser.objects.filter(party=party, user_id=user).delete()
        else:
            PartyUser.objects.update_or_create(party=party, user_id=user, defaults=dict(status=status))
        return Response({}, status=200)


class MapView(generics.GenericAPIView):
    permission_classes = (IsAuthenticatedAndActive,)

    def get(self, request, *args, **kwargs):
        map_type = request.GET.get("type")
        now = timezone.now()
        items = []
        if not map_type or map_type == "party":
            for party in Party.objects.filter(start_date__gte=now, geo__isnull=False, is_deleted=False):
                geometry = party.geo
                geometry["type"] = "Point"
                item = {
                    "id": str(party.pk),
                    "slug": party.slug,
                    "geometry": geometry,
                    "name": party.name,
                    "description": party.short_description,
                    "type": "party",
                    "image": party.image.get_image_url("thumbnail_100x100") if party.image else None,
                }
                items.append(item)
        if not map_type or map_type == "club":
            for club in Club.objects.filter(geo__isnull=False, is_deleted=False, status=Club.STATUS_APPROVED):
                geometry = club.geo
                geometry["type"] = "Point"
                item = {
                    "id": str(club.pk),
                    "slug": club.slug,
                    "geometry": geometry,
                    "name": club.name,
                    "description": club.description,
                    "type": "club",
                    "image": club.image.get_image_url("thumbnail_100x100") if club.image else None,
                }
                items.append(item)
        return Response(items)


class CalendarView(generics.GenericAPIView):
    permission_classes = (IsAuthenticatedAndActive,)

    def get(self, request, *args, **kwargs):
        return Response([])
