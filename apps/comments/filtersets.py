from apps.generic.filtersets import ContentTypeFilter
from django_filters import filterset

from .models import Comment


class CommentFilterSet(filterset.FilterSet):
    content_type = ContentTypeFilter()

    class Meta:
        model = Comment
        fields = ("object_id", "content_type")
