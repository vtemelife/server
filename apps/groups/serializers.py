from apps.generic.choices import ComminityTypeChoices, ThemeChoices
from apps.generic.fields import ChoiceDisplayField
from apps.memberships.models import MembershipRequest
from apps.storage.serializers import ImageSerializer
from apps.users.serializers.profile import UserSerializer
from rest_framework import serializers

from .models import Group


class GroupListSerializer(serializers.ModelSerializer):
    image = ImageSerializer()
    relationship_theme = ChoiceDisplayField(choices=ThemeChoices.THEMES)
    group_type = ChoiceDisplayField(choices=ComminityTypeChoices.TYPES)
    requests_count = serializers.SerializerMethodField()
    request = serializers.SerializerMethodField()

    def get_requests_count(self, obj):
        return obj.requests.filter(status=MembershipRequest.STATUS_WAITING_MODERATION).count()

    def get_request(self, obj):
        user = self.context["request"].user
        request = obj.requests.filter(user=user).first()
        if request:
            return request.pk

    class Meta:
        model = Group
        fields = (
            "pk",
            "slug",
            "name",
            "image",
            "description",
            "relationship_theme",
            "group_type",
            "creator",
            "moderators",
            "users",
            "requests_count",
            "request",
        )


class GroupRetrieveSerializer(GroupListSerializer):
    moderators = UserSerializer(many=True)
    users = UserSerializer(many=True)

    class Meta:
        model = Group
        fields = (
            "pk",
            "slug",
            "name",
            "image",
            "description",
            "relationship_theme",
            "group_type",
            "creator",
            "moderators",
            "users",
            "requests_count",
            "request",
        )


class GroupCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ("pk", "slug", "name", "image", "description", "relationship_theme", "group_type")


class GroupDeleteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ("pk", "slug")


class GroupLeaveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ("pk", "slug")
