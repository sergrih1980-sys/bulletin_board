from rest_framework import viewsets, permissions
from .models import Ad, Review
from .serializers import AdSerializer, ReviewSerializer
from .permissions import IsAdminOrOwner


class AdViewSet(viewsets.ModelViewSet):
    queryset = Ad.objects.filter(is_active=True)
    serializer_class = AdSerializer

    def get_permissions(self):
        """
        Аноним:      только list (список объявлений)
        Авторизованный: list, retrieve, create
        Админ/Владелец: update, partial_update, destroy
        """
        if self.action == 'list':
            return [permissions.AllowAny()]

        if self.action == 'retrieve':
            return [permissions.IsAuthenticated()]

        if self.action == 'create':
            return [permissions.IsAuthenticated()]

        # update, partial_update, destroy
        return [IsAdminOrOwner()]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

    def get_permissions(self):
        """
        Аноним:      list, retrieve (отзывы можно читать всем)
        Авторизованный: create
        Админ/Владелец: update, partial_update, destroy
        """
        if self.action in ['list', 'retrieve']:
            return [permissions.AllowAny()]

        if self.action == 'create':
            return [permissions.IsAuthenticated()]

        # update, partial_update, destroy
        return [IsAdminOrOwner()]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)