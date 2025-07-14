from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TariffViewSet, UserSubscriptionViewSet

router = DefaultRouter()
router.register(r'tariffs', TariffViewSet, basename='tariff')
router.register(r'subscriptions', UserSubscriptionViewSet, basename='subscription')

urlpatterns = [
    path('api/', include(router.urls)),
]
