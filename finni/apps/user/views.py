from datetime import datetime, timedelta, UTC, timezone

import requests

from rest_framework import viewsets, status
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenVerifySerializer
from rest_framework_simplejwt.tokens import RefreshToken

from django_project.settings.base import env
from .models import User
from .schemas import kakao_schema, naver_schema, refresh_schema, verify_schema, logout_schema, update_schema, \
    destroy_schema, retrieve_schema
from .serializers import UserSerializer


class AuthViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        if self.action in ["logout", ]:
            self.permission_classes = [permissions.IsAuthenticated]
        else:
            self.permission_classes = [permissions.AllowAny]

        return super(AuthViewSet, self).get_permissions()

    @kakao_schema
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

    @naver_schema
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
                    "message": "Login successful.",
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

    @refresh_schema
    def refresh(self, request, *args, **kwargs):
        refresh_token = request.COOKIES.get("refresh_token", None)
        refresh_token = RefreshToken(refresh_token)
        new_access_token = str(refresh_token.access_token)
        max_age = (
            datetime.fromtimestamp(refresh_token.get("exp"), timezone.utc) - datetime.now(UTC)
        ).total_seconds()

        res = Response(
            data={
                "code": 20000,
                "message": "Refresh successful.",
                "access_token": new_access_token,
            },
            status=status.HTTP_200_OK,
        )
        res.set_cookie(
            "refresh_token",
            str(refresh_token),
            max_age=max_age,
            secure=True,
            httponly=True,
        )

        return res

    @verify_schema
    def verify(self, request, *args, **kwargs):
        access_token = request.data.get("access_token", None)
        serializer = TokenVerifySerializer(data={"token": access_token})

        try:
            serializer.is_valid(raise_exception=True)
        except Exception as e:
            return Response(
                data={
                    "code": 40000,
                    "message": str(e)
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        return Response(
            {
                "code": 20000,
                "message": "Verified token.",
            },
            status=status.HTTP_200_OK,
        )

    @logout_schema
    def logout(self, request, *args, **kwargs):
        response = Response(status=status.HTTP_205_RESET_CONTENT)
        response.delete_cookie("refresh_token")

        return response


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @retrieve_schema
    def retrieve(self, request, *args, **kwargs):
        response = super(UserViewSet, self).retrieve(request, *args, **kwargs)

        return Response(
            data={
                "code": 20000,
                "message": "User retrieved.",
                "result": {
                    "user": response.data,
                }
            },
            status=status.HTTP_200_OK,
        )

    @update_schema
    def update(self, request, *args, **kwargs):
        response = super(UserViewSet, self).update(request, *args, **kwargs)

        return Response(
            {
                "code": 20000,
                "message": "Updated.",
                "result": {
                    "user": response.data,
                }
            },
            status=status.HTTP_200_OK,
        )

    @destroy_schema
    def destroy(self, request, *args, **kwargs):
        return super(UserViewSet, self).destroy(request, *args, **kwargs)
