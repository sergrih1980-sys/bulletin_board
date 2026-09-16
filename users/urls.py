from django.urls import path
from django.contrib.auth import views as auth_views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import UserViewSet

urlpatterns = [
    path("", UserViewSet.as_view({"get": "list", "post": "create"})),
    path("<int:pk>/", UserViewSet.as_view({
        "get": "retrieve",
        "put": "update",
        "patch": "partial_update",
        "delete": "destroy",
    })),
    path("login/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    # Сброс пароля
    path("reset_password/", auth_views.PasswordResetView.as_view(),
         name="reset_password"),
    path("reset_password_confirm/<uidb64>/<token>/",
         auth_views.PasswordResetConfirmView.as_view(),
         name="password_reset_confirm"),
]