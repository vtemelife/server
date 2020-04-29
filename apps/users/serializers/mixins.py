import datetime

from django.utils.translation import gettext_lazy as _
from rest_framework import serializers


class PasswordMixin:
    def validate_new_password(self, value):
        # TODO
        # if not self.instance.check_password(value):
        #     raise serializers.ValidationError(_("Password is incorrect."))
        return value

    def validate(self, data):
        data = super().validate(data)
        if (
            data.get("new_password")
            and data.get("repeat_new_password")
            and data.get("new_password") != data.get("repeat_new_password")
        ):
            raise serializers.ValidationError({"repeat_new_password": [_("Passwords do not match")]})
        if data.get("new_password") and not data.get("repeat_new_password"):
            raise serializers.ValidationError({"repeat_new_password": [_("Field is required")]})
        if not data.get("new_password") and data.get("repeat_new_password"):
            raise serializers.ValidationError({"new_password": [_("Field is required")]})
        return data

    def save(self, *args, **kwargs):
        new_password = self.validated_data.pop("new_password", None)
        self.validated_data.pop("repeat_new_password", None)
        if new_password:
            self.instance.set_password(new_password)
        return super().save(*args, **kwargs)


class BirthdayMixin:
    def validate(self, data):
        data = super().validate(data)
        min_year = 1940
        max_year = datetime.date.today().year - 18
        value = data.get("birthday")
        if value and (value < min_year or value > max_year):
            raise serializers.ValidationError(
                {"birthday": [_("Birthday should be in range {} - {}".format(min_year, max_year))]}
            )
        value = data.get("birthday_second")
        if value and (value < min_year or value > max_year):
            raise serializers.ValidationError(
                {"birthday_second": [_("Birthday should be in range {} - {}".format(min_year, max_year))]}
            )
        return data
