from django_filters import filterset

from apps.generic.filtersets import ContentTypeFilter

from .models import Comment


class CommentFilterSet(filterset.FilterSet):
    content_type = ContentTypeFilter()

    class Meta:
        model = Comment
        fields = ("object_id", "content_type")
