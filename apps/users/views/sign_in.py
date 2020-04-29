from apps.generic.permissions import IsAuthenticatedAndActive
from apps.users.serializers.sign_in import SignInSerializer, SignInVerifySerializer
from django.contrib.auth import login, logout
from rest_framework import generics
from rest_framework.response import Response


class SignInView(generics.GenericAPIView):
    serializer_class = SignInSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        login(request, serializer.validated_data["user"])
        return Response({"slug": user.slug}, status=200)


class SignInVerifyView(generics.RetrieveAPIView):
    permission_classes = (IsAuthenticatedAndActive,)
    serializer_class = SignInVerifySerializer

    def get_object(self):
        return self.request.user


class SignOutView(generics.GenericAPIView):
    def get_serializer(self, *args, **kwargs):
        return None

    def post(self, request, *args, **kwargs):
        logout(request)
        return Response({}, status=200)
