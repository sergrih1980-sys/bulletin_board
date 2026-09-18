from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from django.conf import settings
from django.conf.urls.static import static

from ads.views import AdViewSet, ReviewViewSet
from users.views import UserProfileView

router = DefaultRouter()
router.register(r'ads', AdViewSet, basename='ad')
router.register(r'reviews', ReviewViewSet, basename='review')
# УБРАЛИ router.register(r'users', ...) — он уже в users/urls.py

urlpatterns = [
    path('admin/', admin.site.urls),

    path('api/users/', include('users.urls')),  # ПОДНЯЛИ ВЫШЕ — me/ и reset_*/ теперь приоритетнее
    path('api/', include(router.urls)),

    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)