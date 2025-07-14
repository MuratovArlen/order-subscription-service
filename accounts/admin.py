from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    fieldsets = UserAdmin.fieldsets + (
        (None, {"fields": ("phone", "telegram_id")}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {"fields": ("phone", "telegram_id")}),
    )
    list_display = ["username", "email", "phone", "telegram_id", "is_staff"]
    search_fields = ["username", "email", "phone"]

admin.site.register(CustomUser, CustomUserAdmin)
