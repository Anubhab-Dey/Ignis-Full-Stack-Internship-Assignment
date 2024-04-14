from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import Event


class CustomUserAdmin(UserAdmin):
    list_display = (
        "username",
        "email",
        "first_name",
        "last_name",
        "is_staff",
        "last_login",
    )
    list_filter = ("is_staff", "is_superuser", "is_active")


admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)


class EventAdmin(admin.ModelAdmin):
    list_display = (
        "event_name",
        "date",
        "time",
        "location",
        "user",
        "is_liked",
    )
    list_filter = ("date", "is_liked", "user")
    search_fields = ("event_name", "location", "user__username")


admin.site.register(Event, EventAdmin)
