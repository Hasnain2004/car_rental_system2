from django.contrib import admin
from .models import Admin, Car, Booking, UserProfile, ContactMessage

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

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'subject', 'created_at', 'is_read')
    list_filter = ('is_read', 'created_at')
    search_fields = ('name', 'email', 'subject', 'message')
    readonly_fields = ('name', 'email', 'subject', 'message', 'created_at')
    ordering = ('-created_at',)
    
    def get_readonly_fields(self, request, obj=None):
        if obj:  # editing an existing object
            return self.readonly_fields + ('is_read',)
        return self.readonly_fields

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser

    def has_add_permission(self, request):
        return False  # Prevent adding messages manually through admin
