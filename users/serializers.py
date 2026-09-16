from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.tokens import default_token_generator
from django.conf import settings
from django.core.mail import send_mail
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "email", "first_name", "last_name", "phone", "image", "role"]
        read_only_fields = ["id", "role"]

    def update(self, instance, validated_data):
        validated_data.pop("role", None)
        return super().update(instance, validated_data)


# --- Сериализаторы для восстановления пароля ---

class PasswordResetRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        # Возвращаем значение всегда, чтобы не раскрывать факт существования пользователя
        return value

    def save(self):
        email = self.validated_data["email"]
        user = User.objects.filter(email=email).first()

        if user:
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))

            # Ссылка (для разработки)
            reset_url = f"http://localhost:8000/password-reset-confirm/{uid}/{token}"

            subject = "Сброс пароля Bulletin Board"
            message = f"Нажмите на ссылку, чтобы сбросить пароль: {reset_url}"

            send_mail(
                subject=subject,
                message=message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[user.email],
                fail_silently=False,
            )
        return self.validated_data


class PasswordResetConfirmSerializer(serializers.Serializer):
    uid = serializers.CharField()
    token = serializers.CharField()
    new_password = serializers.CharField(write_only=True, min_length=8)

    def validate(self, data):
        uid = data.get("uid")
        token = data.get("token")

        try:
            uid_decoded = force_str(urlsafe_base64_decode(uid))
            user = User.objects.get(pk=uid_decoded)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            raise serializers.ValidationError(_("Неверная ссылка для сброса пароля"))

        if not default_token_generator.check_token(user, token):
            raise serializers.ValidationError(_("Токен недействителен или истек"))

        data["user"] = user
        return data

    def save(self):
        user = self.validated_data["user"]
        new_password = self.validated_data["new_password"]
        user.set_password(new_password)
        user.save()
        return user