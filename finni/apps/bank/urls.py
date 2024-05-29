from django.urls import path

from .views import AllowanceViewSet

urlpatterns = [
    path(
        "allowance",
        AllowanceViewSet.as_view({"post": "create"}),
    ),
]
