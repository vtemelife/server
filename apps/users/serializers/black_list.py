from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from apps.users.models import BlackList
from apps.users.serializers.profile import UserSerializer


class BlackListItemSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = BlackList
        fields = ("pk", "user", "reason", "reason_message")


class BlackListCreateSerializer(serializers.ModelSerializer):
    reason_message = serializers.CharField(allow_blank=True)

    def validate_user(self, value):
        creator = self.context["request"].user
        if BlackList.objects.filter(creator=creator, user=value).exists():
            raise serializers.ValidationError(_("You've already added this user to black list"))
        return value

    class Meta:
        model = BlackList
        fields = ("pk", "user", "reason", "reason_message")


class BlackListDeleteSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlackList
        fields = ("pk",)
