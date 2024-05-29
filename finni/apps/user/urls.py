from django.urls import path

from .views import AuthViewSet, UserViewSet

urlpatterns = [
    path(
        "login/kakao/callback",
        AuthViewSet.as_view({"get": "kakao"})
    ),
    path(
        "login/naver/callback",
        AuthViewSet.as_view({"get": "naver"}),
    ),
    path(
        "<int:pk>",
        UserViewSet.as_view({"patch": "update", "delete": "destroy"}),
    ),
    path(
        "token/refresh",
        AuthViewSet.as_view({"post": "refresh"}),
    ),
    path(
        "token/verify",
        AuthViewSet.as_view({"post": "verify"}),
    ),
    path(
        "logout",
        AuthViewSet.as_view({"post": "logout"}),
    ),

]
