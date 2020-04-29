from django.contrib.contenttypes.models import ContentType
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from apps.clubs.models import Club
from apps.clubs.serializers import ClubListSerializer
from apps.generic.fields import ContentTypeField
from apps.groups.models import Group
from apps.groups.serializers import GroupListSerializer
from apps.users.models import User
from apps.users.serializers.profile import ProfileSerializer

from .models import MembershipRequest


class MembershipRequestListItemSerializer(serializers.ModelSerializer):
    user = ProfileSerializer()
    content_type = serializers.SerializerMethodField()
    content_object = serializers.SerializerMethodField()

    def get_content_type(self, obj):
        return "%s:%s" % (obj.content_type.app_label, obj.content_type.model)

    def get_content_object(self, obj):
        serializer = None
        content_object = obj.content_object
        if content_object.__class__.__name__ == "User":
            serializer = ProfileSerializer(content_object, context=self.context)
        elif content_object.__class__.__name__ == "Group":
            serializer = GroupListSerializer(content_object, context=self.context)
        elif content_object.__class__.__name__ == "Club":
            serializer = ClubListSerializer(content_object, context=self.context)
        if serializer:
            return serializer.data

    class Meta:
        model = MembershipRequest
        fields = ("pk", "user", "content_object", "content_type", "status")


class MembershipRequestCreateSerializer(serializers.ModelSerializer):
    content_type = ContentTypeField()

    def validate(self, data):
        object_id = data["object_id"]
        content_type = data["content_type"]
        user = self.context["request"].user

        ct_user = ContentType.objects.get_for_model(User)
        ct_group = ContentType.objects.get_for_model(Group)
        ct_club = ContentType.objects.get_for_model(Club)

        if content_type == ct_user:
            if MembershipRequest.objects.filter(content_type=content_type, object_id=object_id, user=user).exists():
                raise serializers.ValidationError(
                    _("You have already sent request to add this user to friends.")  # noqa
                )
            if MembershipRequest.objects.filter(
                content_type=content_type, object_id=user.pk, user_id=object_id
            ).exists():
                raise serializers.ValidationError(_("User has already sent request to add you to friends."))
        if content_type == ct_group:
            if MembershipRequest.objects.filter(content_type=content_type, object_id=object_id, user=user).exists():
                raise serializers.ValidationError(_("You have already sent request to join this group."))
        if content_type == ct_club:
            if MembershipRequest.objects.filter(content_type=content_type, object_id=object_id, user=user).exists():
                raise serializers.ValidationError(_("You have already sent request to join this club."))
        return data

    class Meta:
        model = MembershipRequest
        fields = ("pk", "object_id", "content_type")


class MembershipRequestUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = MembershipRequest
        fields = ("pk", "status")


class MembershipRequestDeleteSerializer(serializers.ModelSerializer):
    class Meta:
        model = MembershipRequest
        fields = ("pk",)
