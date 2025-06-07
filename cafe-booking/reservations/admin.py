from django.contrib import admin
from .models import Table, Reservation


@admin.register(Table)
class TableAdmin(admin.ModelAdmin):
    list_display = ('number', 'seats', 'shape', 'width', 'length')
    list_filter = ('seats', 'shape')
    search_fields = ('number', 'description')


@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ('customer_name', 'table', 'date', 'time', 'duration', 'confirmed')
    list_filter = ('confirmed', 'date', 'table')
    search_fields = ('customer_name', 'customer_phone', 'customer_email')
    list_editable = ('confirmed',)
    actions = ['confirm_reservations']

    def confirm_reservations(self, request, queryset):
        queryset.update(confirmed=True)

    confirm_reservations.short_description = "Подтвердить выбранные бронирования"