from django.urls import path

from .views import (
    GameDeleteView,
    GameListView,
    GameRetrieveView,
    GameUpdateView,
    GameUserCreateView,
    GameUserRetrieveView,
    GameUserUpdateView,
)

app_name = "apps.games"

urlpatterns = [
    path("", GameListView.as_view(), name="pogamest-list"),
    path("retrieve/<slug:slug>/", GameRetrieveView.as_view(), name="game-retrieve"),
    path("update/<slug:slug>/", GameUpdateView.as_view(), name="game-update"),
    path("delete/<slug:slug>/", GameDeleteView.as_view(), name="game-delete"),
    path("user/retrieve/<uuid:pk>/", GameUserRetrieveView.as_view(), name="game-user-retrieve"),
    path("user/create/", GameUserCreateView.as_view(), name="game-user-create"),
    path("user/update/<uuid:pk>/", GameUserUpdateView.as_view(), name="game-user-update"),
    path("user/delete/<uuid:pk>/", GameUserUpdateView.as_view(), name="game-user-update"),
]
