from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema, no_body


def kakao_schema(view_function):
    schema = swagger_auto_schema(
        tags=["인증"],
        operation_id="카카오 로그인",
        security=[],
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
        },
    )(view_function)

    return schema


def naver_schema(view_function):
    schema = swagger_auto_schema(
        tags=["인증"],
        operation_id="네이버 로그인",
        security=[],
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
                        "access_token": openapi.Schema(type=openapi.TYPE_STRING, description="액세스 토큰"),
                    }
                )
            ),
        }
    )(view_function)

    return schema


def refresh_schema(view_function):
    schema = swagger_auto_schema(
        tags=["토큰"],
        operation_id="토큰 재발급",
        security=[],
        manual_parameters=[
            openapi.Parameter(
                name="refresh_token",
                in_=openapi.IN_HEADER,
                description="The refresh token in cookie",
                type=openapi.TYPE_STRING,
                required=True
            )
        ],
        request_body=no_body,
        responses={
            200: openapi.Response(
                description="OK",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "code": openapi.Schema(type=openapi.TYPE_INTEGER, description="응답 코드"),
                        "message": openapi.Schema(type=openapi.TYPE_STRING, description="응답 메시지"),
                        "access_token": openapi.Schema(type=openapi.TYPE_STRING, description="액세스 토큰"),
                    }
                )
            ),
        }
    )(view_function)

    return schema


def verify_schema(view_function):
    schema = swagger_auto_schema(
        tags=["토큰"],
        operation_id="토큰 검증",
        security=[],
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "access_token": openapi.Schema(type=openapi.TYPE_STRING, description="액세스 토큰"),
            },
            required=["access_token"]
        ),
        responses={
            200: openapi.Response(
                description="OK",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "code": openapi.Schema(type=openapi.TYPE_INTEGER, description="응답 코드"),
                        "message": openapi.Schema(type=openapi.TYPE_STRING, description="응답 메시지"),
                    }
                )
            ),
            400: openapi.Response(
                description="Bad Request",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "code": openapi.Schema(type=openapi.TYPE_INTEGER, description="응답 코드"),
                        "message": openapi.Schema(type=openapi.TYPE_STRING, description="응답 메시지"),
                    }
                )
            ),
        }
    )(view_function)

    return schema


def logout_schema(view_function):
    schema = swagger_auto_schema(
        tags=["인증"],
        operation_id="로그아웃",
        request_body=no_body,
        responses={
            205: openapi.Response(description="Reset Content"),
        }
    )(view_function)

    return schema


def retrieve_schema(view_function):
    schema = swagger_auto_schema(
        tags=["회원"],
        operation_id="회원 조회",
        request_body=no_body,
        responses={
            200: openapi.Response(
                description="OK",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "code": openapi.Schema(type=openapi.TYPE_INTEGER, description="응답 코드"),
                        "message": openapi.Schema(type=openapi.TYPE_STRING, description="응답 메시지"),
                        "result": openapi.Schema(
                            type=openapi.TYPE_OBJECT,
                            properties={
                                "user": openapi.Schema(
                                    type=openapi.TYPE_OBJECT,
                                    properties={
                                        "email": openapi.Schema(type=openapi.TYPE_STRING, description="이메일"),
                                        "name": openapi.Schema(type=openapi.TYPE_STRING, description="이름"),
                                        "birth": openapi.Schema(type=openapi.TYPE_STRING, description="생년월일"),
                                    },
                                    description="유저",
                                ),
                            },
                            description="결과",
                        ),
                    }
                )
            ),
        }
    )(view_function)

    return schema


def update_schema(view_function):
    schema = swagger_auto_schema(
        tags=["회원"],
        operation_id="내 정보 수정",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "name": openapi.Schema(type=openapi.TYPE_STRING, description="이름"),
                "birth": openapi.Schema(type=openapi.TYPE_STRING, description="생년월일"),
            },
        ),
        responses={
            200: openapi.Response(
                description="OK",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "code": openapi.Schema(type=openapi.TYPE_INTEGER, description="응답 코드"),
                        "message": openapi.Schema(type=openapi.TYPE_STRING, description="응답 메시지"),
                        "result": openapi.Schema(
                            type=openapi.TYPE_OBJECT,
                            properties={
                                "user": openapi.Schema(
                                    type=openapi.TYPE_OBJECT,
                                    properties={
                                        "email": openapi.Schema(type=openapi.TYPE_STRING, description="이메일"),
                                        "name": openapi.Schema(type=openapi.TYPE_STRING, description="이름"),
                                        "birth": openapi.Schema(type=openapi.TYPE_STRING, description="생년월일"),
                                    },
                                    description="유저",
                                ),
                            },
                            description="결과",
                        ),
                    }
                )
            ),
        }
    )(view_function)

    return schema


def destroy_schema(view_function):
    schema = swagger_auto_schema(
        tags=["회원"],
        operation_id="회원 탈퇴",
        request_body=no_body,
        responses={
            204: openapi.Response(description="No Content"),
        }
    )(view_function)

    return schema
