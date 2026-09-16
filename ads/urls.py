from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_nested.routers import NestedDefaultRouter
from .views import AdViewSet, ReviewViewSet

router = DefaultRouter()
router.register(r"ads", AdViewSet, basename="ad")

ads_router = NestedDefaultRouter(router, r"ads", lookup="ad")
ads_router.register(r"reviews", ReviewViewSet, basename="ad-reviews")

urlpatterns = [
    path("", include(router.urls)),
    path("", include(ads_router.urls)),
]
