from django.contrib import admin
from .models import Tariff, UserSubscriptions


admin.site.register(Tariff)
admin.site.register(UserSubscriptions)