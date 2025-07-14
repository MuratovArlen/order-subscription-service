from rest_framework import viewsets, permissions
from .models import Tariff, UserSubscriptions
from .serializers import TariffSerializers, UserSubcriptionsSerializers

class TariffViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tariff.objects.all()
    serializer_class = TariffSerializers
    permission_classes = [permissions.AllowAny]


class UserSubscriptionViewSet(viewsets.ModelViewSet):
    queryset = UserSubscriptions.objects.all()
    serializer_class = UserSubcriptionsSerializers
    permission_classes = [permissions.IsAuthenticated]


    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        return serializer.save(user=self.request.user)