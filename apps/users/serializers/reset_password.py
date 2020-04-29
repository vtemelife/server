from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from apps.users.models import User
from apps.users.serializers.mixins import PasswordMixin


class ResetPasswordStep1Serializer(serializers.ModelSerializer):
    def validate_email(self, value):
        if value and not User.objects.filter(email=value).exists():
            raise serializers.ValidationError(_("User doesn't exist with this email"))
        if value and User.objects.filter(email=value, is_active=False).exists():
            raise serializers.ValidationError(
                _(
                    "User is not active. Please finish a registration \
                    or contact with site administration"
                )
            )
        return value

    class Meta:
        model = User
        fields = ("pk", "email")


class ResetPasswordStep2Serializer(PasswordMixin, serializers.ModelSerializer):
    reset_password_key = serializers.IntegerField(write_only=True, required=True)
    new_password = serializers.CharField(write_only=True, required=True)
    repeat_new_password = serializers.CharField(write_only=True, required=True)

    def validate_reset_password_key(self, value):
        if value != self.instance.reset_password_key:
            raise serializers.ValidationError(_("Invalide Code. Please check email and provide valid code"))
        return None

    class Meta:
        model = User
        fields = ("pk", "reset_password_key", "new_password", "repeat_new_password")
