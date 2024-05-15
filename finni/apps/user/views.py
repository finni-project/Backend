from datetime import datetime, timedelta, UTC

import requests

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

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

    @swagger_auto_schema(
        tags=["소셜 로그인"],
        operation_id="카카오 로그인",
        manual_parameters=[
            openapi.Parameter(
                "code",
                openapi.IN_QUERY,
                type=openapi.TYPE_STRING,
                description="인가 코드",
            ),
        ],
        responses={
            200: openapi.Response(
                description="OK",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "code": openapi.Schema(type=openapi.TYPE_INTEGER, description="응답 코드"),
                        "message": openapi.Schema(type=openapi.TYPE_STRING, description="응답 메시지"),
                        "user_email": openapi.Schema(type=openapi.TYPE_STRING, description="유저 이메일"),
                        "access_token": openapi.Schema(type=openapi.TYPE_STRING, description="액세스 토큰"),
                    }
                )
            ),
            201: openapi.Response(
                description="Created",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "code": openapi.Schema(type=openapi.TYPE_INTEGER, description="응답 코드"),
                        "message": openapi.Schema(type=openapi.TYPE_STRING, description="응답 메시지"),
                        "user_email": openapi.Schema(type=openapi.TYPE_STRING, description="유저 이메일"),
                        "access_token": openapi.Schema(type=openapi.TYPE_STRING, description="액세스 토큰"),
                    }
                )
            ),
        }
    )
    def kakao(self, request, *args, **kwargs):
        response = requests.post(
            "https://kauth.kakao.com/oauth/token",
            data={
                "grant_type": "authorization_code",
                "client_id": env("KAKAO_CLIENT_ID"),
                "client_secret": env("KAKAO_CLIENT_SECRET"),
                "redirect_url": f"{env("FRONTEND_URL")}/auth/kakao/callback",
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

    @swagger_auto_schema(
        tags=["소셜 로그인"],
        operation_id="네이버 로그인",
        manual_parameters=[
            openapi.Parameter(
                "code",
                openapi.IN_QUERY,
                type=openapi.TYPE_STRING,
                description="인가 코드",
            ),
        ],
        responses={
            200: openapi.Response(
                description="OK",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "code": openapi.Schema(type=openapi.TYPE_INTEGER, description="응답 코드"),
                        "message": openapi.Schema(type=openapi.TYPE_STRING, description="응답 메시지"),
                        "user_email": openapi.Schema(type=openapi.TYPE_STRING, description="유저 이메일"),
                        "access_token": openapi.Schema(type=openapi.TYPE_STRING, description="액세스 토큰"),
                    }
                )
            ),
            201: openapi.Response(
                description="Created",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "code": openapi.Schema(type=openapi.TYPE_INTEGER, description="응답 코드"),
                        "message": openapi.Schema(type=openapi.TYPE_STRING, description="응답 메시지"),
                        "user_email": openapi.Schema(type=openapi.TYPE_STRING, description="유저"),
                        "access": openapi.Schema(type=openapi.TYPE_STRING, description="액세스 토큰"),
                    }
                )
            ),
        }
    )
    def naver(self, request, *args, **kwargs):
        response = requests.post(
            "https://nid.naver.com/oauth2.0/token",
            data={
                "grant_type": "authorization_code",
                "client_id": env("NAVER_CLIENT_ID"),
                "client_secret": env("NAVER_CLIENT_SECRET"),
                "redirect_url": f"{env("FRONTEND_URL")}/auth/naver/callback",
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
            res = Response(
                {
                    "code": 20100,
                    "message": "Created.",
                    "user_email": user.email,
                    "access_token": str(token.access_token),
                },
                status=status.HTTP_201_CREATED,
                headers=kwargs.get("headers"),
            )
        else:
            res = Response(
                {
                    "code": 20000,
                    "message": "Login Success.",
                    "user_email": user.email,
                    "access_token": str(token.access_token),
                },
                status=status.HTTP_200_OK,
            )

        max_age = 7 * 24 * 60 * 60
        expires = datetime.strftime(
            datetime.now(UTC) + timedelta(seconds=max_age),
            "%a, %d-%b-%Y %H:%M:%S GMT",
        )
        res.set_cookie(
            "refresh_token",
            str(token),
            max_age=max_age,
            expires=expires,
            secure=True,
            httponly=True,
        )

        return res
