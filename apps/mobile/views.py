from apps.generic.permissions import IsAuthenticatedAndActive
from rest_framework import generics

from .models import MobileVersion
from .serializers import VersionSerializer


class VersionRetrieveView(generics.RetrieveAPIView):
    serializer_class = VersionSerializer
    queryset = MobileVersion.objects.filter(is_deleted=False)
    permission_classes = (IsAuthenticatedAndActive,)

    def get_object(self):
        qs = super().get_queryset()
        return qs.first()
