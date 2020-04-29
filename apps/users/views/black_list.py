from apps.generic.permissions import IsAuthenticatedAndActive
from apps.users.models import BlackList
from apps.users.serializers.black_list import (
    BlackListCreateSerializer,
    BlackListDeleteSerializer,
    BlackListItemSerializer,
)
from rest_framework import generics


class BlackListView(generics.ListAPIView):
    serializer_class = BlackListItemSerializer
    permission_classes = (IsAuthenticatedAndActive,)
    search_fields = ("user__slug", "user__email")
    queryset = BlackList.objects.filter(is_deleted=False)

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(creator=self.request.user)


class BlackListCreateView(generics.CreateAPIView):
    permission_classes = (IsAuthenticatedAndActive,)
    serializer_class = BlackListCreateSerializer

    def perform_create(self, serializer):
        instance = serializer.save(creator=self.request.user)
        self.request.user.friends.remove(instance.user)
        instance.user.friends.remove(self.request.user)


class BlackListDeleteView(generics.UpdateAPIView):
    permission_classes = (IsAuthenticatedAndActive,)
    serializer_class = BlackListDeleteSerializer
    queryset = BlackList.objects.filter(is_deleted=False)

    def perform_update(self, serializer):
        instance = serializer.instance
        instance.is_deleted = True
        instance.save(update_fields=("is_deleted",))
        return instance
