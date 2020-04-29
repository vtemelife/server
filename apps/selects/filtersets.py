from cities_light.models import City, Region
from django_filters import filterset

from apps.users.models import User


class RegionFilterSet(filterset.FilterSet):
    class Meta:
        model = Region
        fields = ("country",)


class CityFilterSet(filterset.FilterSet):
    class Meta:
        model = City
        fields = ("region", "country")


class ChatUsersFilterSet(filterset.FilterSet):
    class Meta:
        model = User
        fields = ("user_chats",)
