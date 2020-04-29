from rest_framework import generics

from apps.generic.permissions import IsNotGuest

from .filtersets import ShopFilterSet
from .models import Shop
from .serializers import (
    ShopCreateSerializer,
    ShopDeleteSerializer,
    ShopListSerializer,
    ShopRetrieveSerializer,
    ShopUpdateSerializer,
)


class ShopListView(generics.ListAPIView):
    serializer_class = ShopListSerializer
    queryset = Shop.objects.filter(is_deleted=False)
    permission_classes = (IsNotGuest,)
    filterset_class = ShopFilterSet
    search_fields = ("name", "description")


class ShopRetrieveView(generics.RetrieveAPIView):
    serializer_class = ShopRetrieveSerializer
    queryset = Shop.objects.filter(is_deleted=False)
    permission_classes = (IsNotGuest,)


class ShopCreateView(generics.CreateAPIView):
    serializer_class = ShopCreateSerializer
    queryset = Shop.objects.filter(is_deleted=False)
    permission_classes = (IsNotGuest,)

    def perform_create(self, serializer):
        instance = serializer.save(creator=self.request.user)
        instance.moderators.add(self.request.user)


class ShopUpdateView(generics.UpdateAPIView):
    serializer_class = ShopUpdateSerializer
    queryset = Shop.objects.filter(is_deleted=False)
    permission_classes = (IsNotGuest,)

    def perform_update(self, serializer):
        instance = serializer.save()
        instance.moderators.add(self.request.user)
        instance.users.add(self.request.user)


class ShopDeleteView(generics.UpdateAPIView):
    serializer_class = ShopDeleteSerializer
    queryset = Shop.objects.filter(is_deleted=False)
    permission_classes = (IsNotGuest,)

    def perform_update(self, serializer):
        return serializer.save(is_deleted=True)
