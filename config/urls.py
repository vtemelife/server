from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from rest_framework.documentation import include_docs_urls

urlpatterns = [
    path("api/doc/", include_docs_urls(title="API documentation", public=False)),
    path("api/v1/moderation/", include("apps.management.urls", namespace="moderation")),
    path("api/v1/users/", include("apps.users.urls", namespace="users")),
    path("api/v1/memberships/", include("apps.memberships.urls", namespace="memberships")),
    path("api/v1/storage/", include("apps.storage.urls", namespace="storage")),
    path("api/v1/posts/", include("apps.posts.urls", namespace="posts")),
    path("api/v1/media/", include("apps.media.urls", namespace="media")),
    path("api/v1/shops/", include("apps.shops.urls", namespace="shops")),
    path("api/v1/groups/", include("apps.groups.urls", namespace="groups")),
    path("api/v1/events/", include("apps.events.urls", namespace="events")),
    path("api/v1/clubs/", include("apps.clubs.urls", namespace="clubs")),
    path("api/v1/chats/", include("apps.chat.urls", namespace="chat")),
    path("api/v1/comments/", include("apps.comments.urls", namespace="comments")),
    path("api/v1/news/", include("apps.news.urls", namespace="news")),
    path("api/v1/games/", include("apps.games.urls", namespace="games")),
    path("api/v1/selects/", include("apps.selects.urls", namespace="selects")),
    path("api/v1/notifications/", include("apps.notifications.urls", namespace="notifications")),
    path("api/v1/mobile/", include("apps.mobile.urls", namespace="mobile")),
    path("admin/ckeditor/", include("ckeditor_uploader.urls")),
    path("admin/admin_tools/", include("admin_tools.urls")),
    path("admin/", admin.site.urls),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
