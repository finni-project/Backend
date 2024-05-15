from django.urls import path

from .views import LoginViewSet

urlpatterns = [
    path(
        "login/kakao/callback",
        LoginViewSet.as_view({"get": "kakao"})
    ),
    path(
        "login/naver/callback",
        LoginViewSet.as_view({"get": "naver"}),
    ),
]
