from rest_framework import serializers

from apps.clubs.models import Club
from apps.geo.serializers import CitySerializer
from apps.storage.serializers import ImageSerializer
from apps.users.serializers.profile import UserSerializer


class ClubListSerializer(serializers.ModelSerializer):
    creator = UserSerializer()
    image = ImageSerializer()
    city = CitySerializer()

    class Meta:
        model = Club
        fields = ("pk", "slug", "image", "name", "description", "city", "creator", "status", "is_ban")


class ClubToggleBanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Club
        fields = ("pk",)


class ClubApproveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Club
        fields = ("pk",)


class ClubDeclineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Club
        fields = ("pk",)
