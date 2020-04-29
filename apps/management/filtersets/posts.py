from apps.generic.filtersets import BoolFilter
from apps.posts.models import Post
from django_filters import filterset


class PostFilterSet(filterset.FilterSet):
    is_ban = BoolFilter()
    is_whisper = BoolFilter()

    class Meta:
        model = Post
        fields = ("title", "status", "is_ban", "is_whisper")
