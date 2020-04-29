from apps.clubs.models import Club
from apps.generic.choices import ComminityTypeChoices, ThemeChoices
from apps.generic.fields import ChoiceDisplayField
from apps.geo.serializers import CitySerializer
from apps.storage.serializers import ImageSerializer
from apps.users.models import User
from apps.users.serializers.profile import UserSerializer
from django.conf import settings
from rest_framework import serializers

from .models import Party, PartyUser


class ClubPartySerializer(serializers.ModelSerializer):
    moderators = UserSerializer(many=True)

    class Meta:
        model = Club
        fields = ("pk", "slug", "name", "moderators")


class PartyListSerializer(serializers.ModelSerializer):
    image = ImageSerializer()
    city = CitySerializer()
    club = ClubPartySerializer()
    theme = ChoiceDisplayField(choices=ThemeChoices.THEMES)
    party_type = ChoiceDisplayField(choices=ComminityTypeChoices.TYPES)
    users = serializers.SerializerMethodField()
    user_status = serializers.SerializerMethodField()

    def get_users(self, obj):
        # TODO optimization
        return (
            PartyUser.objects.filter(party=obj)
            .exclude(status__in=(PartyUser.STATUS_UNKNOWN,))
            .values_list("user_id", flat=True)
        )

    def get_user_status(self, obj):
        # TODO optimization
        user = self.context["request"].user
        party_user = PartyUser.objects.filter(party=obj, user=user).first()
        if party_user:
            return party_user.status
        else:
            return PartyUser.STATUS_UNKNOWN

    class Meta:
        model = Party
        fields = (
            "pk",
            "slug",
            "club",
            "name",
            "image",
            "short_description",
            "description",
            "party_type",
            "city",
            "users",
            "views",
            "likes",
            "comments_count",
            "hash_tags",
            "theme",
            "start_date",
            "end_date",
            "city",
            "address",
            "geo",
            "status",
            "user_status",
        )


class PartyRetrieveSerializer(PartyListSerializer):
    pair_count = serializers.SerializerMethodField()
    man_count = serializers.SerializerMethodField()
    woman_count = serializers.SerializerMethodField()

    def get_pair_count(self, obj):
        return PartyUser.objects.filter(
            party=obj, user__gender__in=(User.GENDER_MM, User.GENDER_FAMILY, User.GENDER_MW, User.GENDER_WW)
        ).count()

    def get_man_count(self, obj):
        return PartyUser.objects.filter(party=obj, user__gender__in=(User.GENDER_M, User.GENDER_TRANS)).count()

    def get_woman_count(self, obj):
        return PartyUser.objects.filter(party=obj, user__gender__in=(User.GENDER_W, User.GENDER_TRANS)).count()

    class Meta:
        model = Party
        fields = (
            "pk",
            "slug",
            "club",
            "name",
            "image",
            "short_description",
            "description",
            "party_type",
            "city",
            "users",
            "views",
            "likes",
            "comments_count",
            "hash_tags",
            "theme",
            "start_date",
            "end_date",
            "city",
            "address",
            "geo",
            "man_cost",
            "woman_cost",
            "pair_cost",
            "status",
            "user_status",
            "pair_count",
            "man_count",
            "woman_count",
        )


class PartyCreateUpdateSerializer(serializers.ModelSerializer):
    start_date = serializers.DateTimeField(format=settings.DATETIME_FORMAT)
    end_date = serializers.DateTimeField(format=settings.DATETIME_FORMAT)

    class Meta:
        model = Party
        fields = (
            "pk",
            "slug",
            "club",
            "name",
            "image",
            "short_description",
            "description",
            "hash_tags",
            "theme",
            "start_date",
            "end_date",
            "party_type",
            "city",
            "address",
            "geo",
            "man_cost",
            "woman_cost",
            "pair_cost",
        )


class PartyDeleteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Party
        fields = ("pk", "slug")


class PartyLikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Party
        fields = ("pk", "slug", "likes")
        read_only_fields = ("likes",)


class PartyApplySerializer(serializers.Serializer):
    user = serializers.UUIDField()
    status = serializers.CharField()
