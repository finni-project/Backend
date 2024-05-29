from rest_framework import viewsets, permissions, status
from rest_framework.response import Response

from .models import Allowance
from .schemas import create_schema
from .serializers import AllowanceSerializer


class AllowanceViewSet(viewsets.ModelViewSet):
    queryset = Allowance.objects.all()
    serializer_class = AllowanceSerializer
    permission_classes = [permissions.AllowAny]

    @create_schema
    def create(self, request, *args, **kwargs):
        response = super(AllowanceViewSet, self).create(request, *args, **kwargs)

        return Response(
            {
                "code": 20100,
                "message": "Created.",
                "result": {
                    "allowance": response.data,
                }
            },
            status=status.HTTP_201_CREATED,
        )
