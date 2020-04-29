from cities_light.models import City, Country, Region
from rest_framework import serializers

from .utils import get_name


class CountrySerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()

    def get_name(self, obj):
        request = self.context["request"]
        locale = request.LANGUAGE_CODE
        return get_name(obj, locale)

    class Meta:
        model = Country
        fields = ("pk", "name")


class RegionSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()

    def get_name(self, obj):
        request = self.context["request"]
        locale = request.GET.get("locale") or request.LANGUAGE_CODE
        return get_name(obj, locale)

    class Meta:
        model = Region
        fields = ("pk", "name")


class CitySerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    region = RegionSerializer()
    country = CountrySerializer()

    def get_name(self, obj):
        request = self.context["request"]
        locale = request.LANGUAGE_CODE
        return get_name(obj, locale)

    class Meta:
        model = City
        fields = ("pk", "name", "region", "country", "latitude", "longitude")
