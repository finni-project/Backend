from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema, no_body


def create_schema(view_function):
    schema = swagger_auto_schema(
        tags=["용돈"],
        operation_id="용돈 정보 생성",
        responses={
            201: openapi.Response(
                description="Created",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "code": openapi.Schema(type=openapi.TYPE_INTEGER, description="응답 코드"),
                        "message": openapi.Schema(type=openapi.TYPE_STRING, description="응답 메시지"),
                        "result": openapi.Schema(
                            type=openapi.TYPE_OBJECT,
                            properties={
                                "allowance": openapi.Schema(
                                    type=openapi.TYPE_OBJECT,
                                    properties={
                                        "user": openapi.Schema(type=openapi.TYPE_INTEGER, description="회원"),
                                        "cycle": openapi.Schema(type=openapi.TYPE_INTEGER, description="용돈 주기"),
                                        "amount": openapi.Schema(type=openapi.TYPE_INTEGER, description="용돈 금액"),
                                        "allowance_categories": openapi.Schema(
                                            type=openapi.TYPE_ARRAY,
                                            items=openapi.Schema(
                                                type=openapi.TYPE_OBJECT,
                                                properties={
                                                    "name": openapi.Schema(type=openapi.TYPE_STRING, description="이름"),
                                                    "icon": openapi.Schema(type=openapi.TYPE_STRING, description="이모지"),
                                                }
                                            ),
                                            description="용돈 분류",
                                        )
                                    },
                                    description="용돈 정보",
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
