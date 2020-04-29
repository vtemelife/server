from cities_light.models import City, Country, Region
from rest_framework import generics

from apps.clubs.models import Club
from apps.generic.permissions import IsAuthenticatedAndActive
from apps.geo.serializers import CitySerializer, CountrySerializer, RegionSerializer
from apps.users.models import User

from .filtersets import ChatUsersFilterSet, CityFilterSet, RegionFilterSet
from .serializers import ClubSelectSerializer, UserSelectSerializer


class ListSelectView(generics.ListAPIView):
    order_by = None
    limit = 100

    def filter_queryset(self, qs):
        qs = super().filter_queryset(qs)
        if self.order_by:
            qs = qs.order_by(self.order_by)
        return qs[: self.limit]


class CountrySelectView(ListSelectView):
    pagination_class = None
    serializer_class = CountrySerializer
    queryset = Country.objects.all()
    search_fields = ("name", "alternate_names")
    order_by = "name"


class RegionSelectView(ListSelectView):
    pagination_class = None
    serializer_class = RegionSerializer
    queryset = Region.objects.all()
    filterset_class = RegionFilterSet
    search_fields = ("name", "alternate_names")
    order_by = "name"


class CitySelectView(ListSelectView):
    pagination_class = None
    serializer_class = CitySerializer
    queryset = City.objects.all()
    filterset_class = CityFilterSet
    search_fields = ("name", "alternate_names")
    order_by = "name"


class ModeratorsSelectView(generics.ListAPIView):
    pagination_class = None
    permission_classes = (IsAuthenticatedAndActive,)
    serializer_class = UserSelectSerializer
    queryset = User.objects.filter(is_active=True, is_deleted=False, role=User.ROLE_MODERATOR)
    search_fields = ("slug", "name", "email")

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.exclude(pk=self.request.user.pk)


class ChatModeratorsSelectView(generics.ListAPIView):
    pagination_class = None
    permission_classes = (IsAuthenticatedAndActive,)
    serializer_class = UserSelectSerializer
    queryset = User.objects.none()
    search_fields = ("slug", "name", "email")

    def get_queryset(self):
        user = self.request.user
        qs = user.friends.filter(is_active=True, is_deleted=False)
        qs = qs.exclude(black_list__pk=user.pk)
        return qs


class ChatUsersSelectView(generics.ListAPIView):
    pagination_class = None
    permission_classes = (IsAuthenticatedAndActive,)
    serializer_class = UserSelectSerializer
    queryset = User.objects.none()
    search_fields = ("slug", "name", "email")
    filterset_class = ChatUsersFilterSet

    def get_queryset(self):
        user = self.request.user
        qs = user.friends.filter(is_active=True, is_deleted=False)
        qs = qs.exclude(black_list__pk=user.pk)
        return qs


class ClubsSelectView(generics.ListAPIView):
    pagination_class = None
    permission_classes = (IsAuthenticatedAndActive,)
    serializer_class = ClubSelectSerializer
    queryset = Club.objects.filter(is_deleted=False)
    search_fields = ("name",)

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(moderators=self.request.user)
