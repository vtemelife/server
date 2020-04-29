from rest_framework import generics

from apps.users.models import User
from apps.users.serializers.sign_up import SignUpStep1Serializer, SignUpStep2Serializer


class SignUpStep1View(generics.CreateAPIView):
    serializer_class = SignUpStep1Serializer


class SignUpStep2View(generics.UpdateAPIView):
    serializer_class = SignUpStep2Serializer
    queryset = User.objects.filter(is_active=False)

    def perform_update(self, serializer):
        serializer.save(is_active=True)
