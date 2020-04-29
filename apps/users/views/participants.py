from apps.generic.permissions import IsAuthenticatedAndActive
from apps.users.filtersets.friends import FriendListFilterSet as ParticipantFilterSet
from apps.users.models import User
from apps.users.serializers.participants import ParticipantListItemSerializer
from rest_framework import generics


class ParticipantListView(generics.ListAPIView):
    serializer_class = ParticipantListItemSerializer
    permission_classes = (IsAuthenticatedAndActive,)
    filterset_class = ParticipantFilterSet
    search_fields = ("slug", "email")

    def get_queryset(self):
        object_id = self.request.GET.get("object_id")
        content_type = self.request.GET.get("content_type")
        if not object_id or content_type not in (
            "users:user",
            "groups:group",
            "clubs:club",
            "events:party",
            "chats:chat",
        ):
            return User.objects.none()
        qs = User.objects.filter(is_active=True, is_deleted=False).with_online()
        if content_type == "users:user":
            user = qs.filter(pk=object_id).first()
            if user:
                return user.friends.filter(is_active=True, is_deleted=False).with_online()
        if content_type == "chats:chat":
            return qs.filter(user_chats__pk=object_id).distinct()
        if content_type == "groups:group":
            return qs.filter(user_groups__pk=object_id).distinct()
        if content_type == "clubs:club":
            return qs.filter(user_clubs__pk=object_id).distinct()
        if content_type == "events:party":
            return qs.filter(partyuser__party__pk=object_id).distinct()
        return qs.none()
