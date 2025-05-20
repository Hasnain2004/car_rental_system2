from django.contrib import admin
from .models import Admin, Car, Booking

@admin.register(Admin)
class AdminAdmin(admin.ModelAdmin):
    list_display = ('username', 'last_login')
    search_fields = ('username',)

@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    list_display = ('make', 'model', 'year', 'price_per_day', 'available', 'category')
    list_filter = ('available', 'category', 'make')
    search_fields = ('make', 'model')

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('user', 'car', 'booking_date', 'return_date', 'total_price', 'status')
    list_filter = ('status', 'booking_date')
    search_fields = ('user__username', 'car__make', 'car__model')
