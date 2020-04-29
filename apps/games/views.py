from apps.generic.permissions import IsAuthenticatedAndActive
from django.core.exceptions import PermissionDenied
from django.db.models import F, Q
from rest_framework import generics

from .filtersets import GameFilterSet
from .models import Game, GameUser
from .serializers import (
    GameDeleteSerializer,
    GameItemSerializer,
    GameSerializer,
    GameUpdateSerializer,
    GameUserCreateSerializer,
    GameUserDeleteSerializer,
    GameUserRetrieveSerializer,
    GameUserUpdateSerializer,
)


class GameListView(generics.ListAPIView):
    serializer_class = GameItemSerializer
    queryset = Game.objects.filter(is_deleted=False).order_by("-created_date")
    permission_classes = (IsAuthenticatedAndActive,)
    filterset_class = GameFilterSet
    search_fields = ("name", "description")

    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.filter(Q(creator=self.request.user) | Q(status=Game.STATUS_APPROVED))
        return qs.distinct()


class GameRetrieveView(generics.RetrieveAPIView):
    serializer_class = GameSerializer
    queryset = Game.objects.filter(is_deleted=False)
    permission_classes = (IsAuthenticatedAndActive,)
    lookup_field = "slug"

    def get_object(self, *args, **kwargs):
        obj = super().get_object(*args, **kwargs)
        obj.views += 1
        Game.objects.filter(pk=obj.pk).update(views=F("views") + 1)
        return obj


class GameUpdateView(generics.UpdateAPIView):
    serializer_class = GameUpdateSerializer
    queryset = Game.objects.filter(is_deleted=False)
    permission_classes = (IsAuthenticatedAndActive,)
    lookup_field = "slug"

    def check_object_permissions(self, request, obj):
        if obj.creator_id != request.user.pk:
            raise PermissionDenied


class GameDeleteView(generics.UpdateAPIView):
    serializer_class = GameDeleteSerializer
    queryset = Game.objects.filter(is_deleted=False)
    permission_classes = (IsAuthenticatedAndActive,)
    lookup_field = "slug"

    def check_object_permissions(self, request, obj):
        if obj.creator_id != request.user.pk:
            raise PermissionDenied

    def perform_update(self, serializer):
        return serializer.save(is_deleted=True)


class GameUserRetrieveView(generics.RetrieveAPIView):
    serializer_class = GameUserRetrieveSerializer
    permission_classes = (IsAuthenticatedAndActive,)
    queryset = GameUser.objects.filter(is_deleted=False, game__is_deleted=False)

    def check_object_permissions(self, request, obj):
        if obj.user_id != request.user.pk:
            raise PermissionDenied


class GameUserCreateView(generics.CreateAPIView):
    serializer_class = GameUserCreateSerializer
    permission_classes = (IsAuthenticatedAndActive,)

    def perform_create(self, serializer):
        return serializer.save(user=self.request.user)


class GameUserUpdateView(generics.UpdateAPIView):
    serializer_class = GameUserUpdateSerializer
    permission_classes = (IsAuthenticatedAndActive,)
    queryset = GameUser.objects.filter(is_deleted=False, game__is_deleted=False)

    def check_object_permissions(self, request, obj):
        if obj.user_id != request.user.pk:
            raise PermissionDenied


class GameUserDeleteView(generics.UpdateAPIView):
    serializer_class = GameUserDeleteSerializer
    queryset = Game.objects.filter(is_deleted=False)
    permission_classes = (IsAuthenticatedAndActive,)

    def check_object_permissions(self, request, obj):
        if obj.user_id != request.user.pk:
            raise PermissionDenied

    def perform_update(self, serializer):
        return serializer.save(is_deleted=True)
