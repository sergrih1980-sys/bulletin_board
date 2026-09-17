from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    UserProfileView,
    PasswordResetView,
    PasswordResetConfirmView,
    UserViewSet,
)

router = DefaultRouter()
router.register(r"", UserViewSet, basename="user")

urlpatterns = [
    path("me/", UserProfileView.as_view(), name="user-profile"),
    path("reset_password/", PasswordResetView.as_view(), name="reset_password"),
    path("reset_password_confirm/", PasswordResetConfirmView.as_view(),
         name="reset_password_confirm"),
    path("", include(router.urls)),
]