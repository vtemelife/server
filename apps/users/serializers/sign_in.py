from django.contrib.auth import authenticate
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from apps.geo.serializers import CitySerializer
from apps.storage.serializers import ImageSerializer
from apps.users.models import User


class SignInSerializer(serializers.Serializer):
    email_or_slug = serializers.CharField()
    password = serializers.CharField(style={"input_type": "password"}, write_only=True)

    def validate(self, attrs):
        email_or_slug = attrs["email_or_slug"]
        password = attrs["password"]

        request = self.context["request"]
        user = authenticate(request, email=email_or_slug, password=password)
        if user is None or user.is_deleted:
            raise ValidationError(_("Credentials are invalid."))
        attrs["user"] = user
        return attrs


class SignInVerifySerializer(serializers.ModelSerializer):
    avatar = ImageSerializer()
    city = CitySerializer()

    class Meta:
        model = User
        fields = ("pk", "slug", "name", "email", "role", "is_real", "avatar", "city", "black_list")
