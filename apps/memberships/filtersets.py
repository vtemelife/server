from django_filters import filterset

from apps.generic.filtersets import ContentTypeFilter

from .models import MembershipRequest


class MembershipRequestFilterSet(filterset.FilterSet):
    content_type = ContentTypeFilter()

    class Meta:
        model = MembershipRequest
        fields = ("user", "object_id", "content_type", "status")
