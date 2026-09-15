from rest_framework import viewsets, permissions
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from .models import Ad, Review
from .serializers import AdSerializer, AdDetailSerializer, ReviewSerializer
from .permissions import IsOwnerOrAdmin


class AdViewSet(viewsets.ModelViewSet):
    queryset = Ad.objects.all()
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, SearchFilter]
    search_fields = ['title']
    filterset_fields = ['is_active']

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return AdDetailSerializer
        return AdSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_permissions(self):
        if self.action in ['update', 'partial_update', 'destroy']:
            return [IsOwnerOrAdmin()]
        return [permissions.IsAuthenticatedOrReadOnly()]


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Review.objects.filter(ad_id=self.kwargs.get('ad_pk'))

    def perform_create(self, serializer):
        ad = Ad.objects.get(pk=self.kwargs.get('ad_pk'))
        serializer.save(author=self.request.user, ad=ad)

    def get_permissions(self):
        if self.action in ['update', 'partial_update', 'destroy']:
            return [IsOwnerOrAdmin()]
        return [permissions.IsAuthenticated()]