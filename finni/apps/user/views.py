import requests

from rest_framework import viewsets, status
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from django_project.settings.base import env
from .models import User
from .serializers import UserSerializer


class LoginViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.AllowAny]
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def kakao(self, request, *args, **kwargs):
        response = requests.post(
            "https://kauth.kakao.com/oauth/token",
            data={
                "grant_type": "authorization_code",
                "client_id": env("KAKAO_CLIENT_ID"),
                "client_secret": env("KAKAO_CLIENT_SECRET"),
                "redirect_url": f"{request.build_absolute_uri("/")}user/login/kakao/callback",
                "code": request.query_params.get("code"),
            }
        )
        response.raise_for_status()
        access_token = response.json().get("access_token")

        user_response = requests.get(
            "https://kapi.kakao.com/v2/user/me",
            headers={
                "Authorization": "Bearer " + access_token,
                "Content-type": "application/x-www-form-urlencoded"
            },
        )
        user_response.raise_for_status()
        user_info = user_response.json().get("kakao_account")

        try:
            user = User.objects.get(email=user_info["email"])
            kwargs["user"] = user

            return self.login(request, *args, **kwargs)
        except User.DoesNotExist:
            kwargs = {
                "email": user_info["email"],
                "name": user_info["profile"]["nickname"]
            }

            return self.create(request, *args, **kwargs)

    def naver(self, request, *args, **kwargs):
        response = requests.post(
            "https://nid.naver.com/oauth2.0/token",
            data={
                "grant_type": "authorization_code",
                "client_id": env("NAVER_CLIENT_ID"),
                "client_secret": env("NAVER_CLIENT_SECRET"),
                "redirect_url": f"{request.build_absolute_uri("/")}user/login/naver/callback",
                "code": request.query_params.get("code"),
                "state": "naver_login",
            },
        )
        response.raise_for_status()
        access_token = response.json().get("access_token")

        user_response = requests.get(
            "https://openapi.naver.com/v1/nid/me",
            headers={
                "Authorization": "Bearer " + access_token
            }
        )
        user_response.raise_for_status()
        user_info = user_response.json()

        try:
            user = User.objects.get(email=user_info["response"]["email"])
            kwargs["user"] = user

            return self.login(request, *args, **kwargs)
        except User.DoesNotExist:
            kwargs = user_info["response"]

            return self.create(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=kwargs)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        kwargs["headers"] = headers
        user = User.objects.get(email=kwargs["email"])
        kwargs["user"] = user

        return self.login(request, *args, **kwargs)

    def login(self, request, *args, **kwargs):
        user = kwargs.get("user")
        token = TokenObtainPairSerializer.get_token(user)

        if kwargs.get("headers"):
            return Response(
                {
                    "user": user.email,
                    "code": 20100,
                    "message": "Created.",
                    "token": {
                        "access": str(token.access_token),
                        "refresh": str(token),
                    },
                },
                status=status.HTTP_201_CREATED,
                headers=kwargs.get("headers"),
            )
        else:
            return Response(
                {
                    "user": user.email,
                    "code": 20000,
                    "message": "Login.",
                    "token": {
                        "access": str(token.access_token),
                        "refresh": str(token),
                    },
                },
                status=status.HTTP_200_OK,
            )
