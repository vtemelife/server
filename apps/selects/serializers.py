from apps.clubs.models import Club
from apps.users.models import User
from rest_framework import serializers


class UserSelectSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("pk", "name")


class ClubSelectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Club
        fields = ("pk", "name")
