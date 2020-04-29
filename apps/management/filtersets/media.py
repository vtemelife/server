from django_filters import filterset

from apps.generic.filtersets import BoolFilter
from apps.media.models import Media


class MediaFilterSet(filterset.FilterSet):
    is_ban = BoolFilter()

    class Meta:
        model = Media
        fields = ("title", "status", "is_ban")
