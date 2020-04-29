from rest_framework import serializers

from apps.generic.choices import ThemeChoices
from apps.generic.fields import ChoiceDisplayField
from apps.geo.serializers import CitySerializer
from apps.storage.serializers import ImageSerializer
from apps.users.models import User
from apps.users.serializers.profile import UserSerializer


class UserListSerializer(serializers.ModelSerializer):
    city = CitySerializer()
    role = ChoiceDisplayField(choices=User.ROLES)
    approver = UserSerializer()
    avatar = ImageSerializer()
    role = ChoiceDisplayField(choices=User.ROLES)
    gender = ChoiceDisplayField(choices=User.GENDERS)
    relationship_formats = ChoiceDisplayField(choices=User.FORMATS)
    relationship_themes = ChoiceDisplayField(choices=ThemeChoices.THEMES)

    class Meta:
        model = User
        fields = (
            "pk",
            "slug",
            "name",
            "avatar",
            "email",
            "is_real",
            "approver",
            "role",
            "about",
            "is_ban",
            "gender",
            "relationship_formats",
            "relationship_themes",
            "birthday",
            "birthday_second",
            "city",
        )


class UserToggleBanSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("pk",)


class UserSetMemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("pk",)


class UserSetRealSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("pk",)
