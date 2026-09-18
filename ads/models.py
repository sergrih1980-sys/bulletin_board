from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MinLengthValidator


class Ad(models.Model):
    title = models.CharField(
        max_length=255,
        validators=[MinLengthValidator(1, "Заголовок не может быть пустым.")]
    )
    price = models.IntegerField(
        validators=[MinValueValidator(0)]
    )
    description = models.TextField()
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='ads'
    )
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title


class Review(models.Model):
    text = models.TextField()
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='reviews',
    )
    ad = models.ForeignKey(
        Ad,
        on_delete=models.CASCADE,
        related_name='reviews',
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'Отзыв от {self.author.email} к "{self.ad.title}"'

