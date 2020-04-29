from rest_framework import serializers

from apps.generic.choices import ComminityTypeChoices, ThemeChoices
from apps.generic.fields import ChoiceDisplayField
from apps.geo.serializers import CitySerializer
from apps.memberships.models import MembershipRequest
from apps.storage.serializers import ImageSerializer
from apps.users.serializers.profile import UserSerializer

from .models import Club


class ClubListSerializer(serializers.ModelSerializer):
    image = ImageSerializer()
    relationship_theme = ChoiceDisplayField(choices=ThemeChoices.THEMES)
    club_type = ChoiceDisplayField(choices=ComminityTypeChoices.TYPES)
    requests_count = serializers.SerializerMethodField()
    request = serializers.SerializerMethodField()
    city = CitySerializer()

    def get_requests_count(self, obj):
        return obj.requests.filter(status=MembershipRequest.STATUS_WAITING_MODERATION).count()

    def get_request(self, obj):
        user = self.context["request"].user
        request = obj.requests.filter(user=user).first()
        if request:
            return request.pk

    class Meta:
        model = Club
        fields = (
            "pk",
            "slug",
            "name",
            "image",
            "description",
            "relationship_theme",
            "club_type",
            "city",
            "address",
            "geo",
            "status",
            "creator",
            "moderators",
            "users",
            "requests_count",
            "request",
        )


class ClubRetrieveSerializer(ClubListSerializer):
    moderators = UserSerializer(many=True)
    users = UserSerializer(many=True)

    class Meta:
        model = Club
        fields = (
            "pk",
            "slug",
            "name",
            "image",
            "description",
            "relationship_theme",
            "club_type",
            "city",
            "address",
            "geo",
            "status",
            "creator",
            "moderators",
            "users",
            "requests_count",
            "request",
        )


class ClubCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Club
        fields = (
            "pk",
            "slug",
            "name",
            "image",
            "description",
            "relationship_theme",
            "club_type",
            "city",
            "address",
            "geo",
        )


class ClubDeleteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Club
        fields = ("pk", "slug")


class ClubLeaveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Club
        fields = ("pk", "slug")
