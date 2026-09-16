from rest_framework import generics, permissions, status
from rest_framework.response import Response
from .serializers import (
    UserSerializer,
    PasswordResetRequestSerializer,
    PasswordResetConfirmSerializer,
)


class UserProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user

    def put(self, request, *args, **kwargs):
        data = request.data.copy()
        data.pop('is_staff', None)
        data.pop('is_superuser', None)

        obj = self.get_object()
        serializer = self.get_serializer(obj, data=data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    def patch(self, request, *args, **kwargs):
        data = request.data.copy()
        data.pop('is_staff', None)
        data.pop('is_superuser', None)

        obj = self.get_object()
        serializer = self.get_serializer(obj, data=data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)


class PasswordResetView(generics.GenericAPIView):
    """POST /api/users/reset_password/ — отправка письма со ссылкой."""
    serializer_class = PasswordResetRequestSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {"detail": "Если такой email существует, письмо для сброса было отправлено."},
            status=status.HTTP_200_OK,
        )


class PasswordResetConfirmView(generics.GenericAPIView):
    """POST /api/users/reset_password_confirm/ — установка нового пароля."""
    serializer_class = PasswordResetConfirmSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {"detail": "Пароль успешно сброшен."},
            status=status.HTTP_200_OK,
        )