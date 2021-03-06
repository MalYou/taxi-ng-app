from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DefaultUserAdmin

from .models import User, Trip


@admin.register(User)
class UserAdmin(DefaultUserAdmin):
    pass


@admin.register(Trip)
class TripAdmin(admin.ModelAdmin):
    fields = (
        'id', 'pick_up_address', 'drop_off_address',
        'driver', 'rider',
        'status', 'created', 'updated',
    )

    list_display = (
        'id', 'pick_up_address', 'drop_off_address',
        'driver', 'rider',
        'status', 'created', 'updated',
    )

    list_filter = (
        'status', 'created', 'updated',
    )

    readonly_fields = ('id', 'created', 'updated')
