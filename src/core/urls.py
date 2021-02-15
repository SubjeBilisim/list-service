from django.urls import path, include
from rest_framework import routers

from . import api
from .views import ListFollowingView,ViewCountView


urlpatterns = (
    path(
        "list/follow/<user_id>/<list_id>/",
        ListFollowingView.as_view(),
        name="listfollow",
    ),
    path(
        "<list_id>/",
        api.SocialListViewSet.as_view(
            {"get": "retrieve", "put": "update", "delete": "destroy"}
        ),
        name="social-list-actions",
    ),
    path(
        "",
        api.SocialListViewSet.as_view({"post": "create"}),
        name="social-list-actions",
    ),
    path(
        "view/count/<list_id>/",
        ViewCountView.as_view(),
        name="social-list-actions",
    ),
)
