from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from django.conf import settings
from django.conf.urls.static import static

from ads.views import AdViewSet, ReviewViewSet
from users.views import UserProfileView  # Импортируем только профиль

router = DefaultRouter()
router.register(r'ads', AdViewSet, basename='ad')
router.register(r'reviews', ReviewViewSet, basename='review')
# УБРАЛИ: router.register(r'users', UserViewSet, ...)

urlpatterns = [
    path('admin/', admin.site.urls),

    # API
    path('api/', include(router.urls)),

    # Личный профиль: только текущий пользователь, менять роли нельзя
    path('api/profile/', UserProfileView.as_view(), name='profile'),

    # JWT
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # Swagger
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

