from apps.mail.mails import ResetPasswordVerification
from apps.users.models import User
from apps.users.serializers.reset_password import ResetPasswordStep1Serializer, ResetPasswordStep2Serializer
from django.utils.crypto import get_random_string
from rest_framework import generics


class ResetPasswordStep1View(generics.UpdateAPIView):
    serializer_class = ResetPasswordStep1Serializer
    queryset = User.objects.all()

    def get_object(self):
        qs = self.get_queryset()
        return qs.filter(email=self.request.data["email"]).first()

    def perform_update(self, serializer):
        instance = serializer.save()
        reset_password_key = int(get_random_string(length=6, allowed_chars="1234567890"))
        instance.reset_password_key = reset_password_key
        instance.save(update_fields=("reset_password_key",))
        ResetPasswordVerification(instance).send(
            context={
                "code": instance.reset_password_key,
                "reset_password": "https://vteme.life/auth/reset-password/finish/%s/" % instance.pk,
            }
        )
        return instance


class ResetPasswordStep2View(generics.UpdateAPIView):
    serializer_class = ResetPasswordStep2Serializer
    queryset = User.objects.filter(reset_password_key__isnull=False)

    def perform_update(self, serializer):
        instance = serializer.save()
        instance.reset_password_key = None
        instance.save(update_fields=("reset_password_key",))
