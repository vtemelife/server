from rest_framework import serializers

from apps.events.models import Party
from apps.geo.serializers import CitySerializer
from apps.storage.serializers import ImageSerializer


class PartyListSerializer(serializers.ModelSerializer):
    image = ImageSerializer()
    city = CitySerializer()

    class Meta:
        model = Party
        fields = ("pk", "slug", "image", "name", "description", "city", "status", "is_ban")


class PartyToggleBanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Party
        fields = ("pk",)


class PartyApproveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Party
        fields = ("pk",)


class PartyDeclineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Party
        fields = ("pk",)
