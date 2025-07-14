from rest_framework import serializers
from .models import Tariff, UserSubscriptions


class TariffSerializers(serializers.ModelSerializer):
    class Meta:
        model = Tariff
        fields = '__all__'


class UserSubcriptionsSerializers(serializers.ModelSerializer):
    class Meta:
        model = UserSubscriptions
        fields = '__all__'