from django.urls import path

from .views import NewsDeleteView, NewsLikeView, NewsListView, NewsRetrieveView

app_name = "apps.news"

urlpatterns = [
    path("", NewsListView.as_view(), name="news-list"),
    path("<uuid:pk>/", NewsRetrieveView.as_view(), name="news-retrieve"),
    path("<uuid:pk>/delete/", NewsDeleteView.as_view(), name="news-delete"),
    path("<slug:pk>/like/", NewsLikeView.as_view(), name="news-like"),
]
