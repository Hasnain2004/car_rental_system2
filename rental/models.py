from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Admin(models.Model):
    username = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=100)
    last_login = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.username

class Car(models.Model):
    make = models.CharField(max_length=50)
    model = models.CharField(max_length=50)
    year = models.IntegerField()
    price_per_day = models.DecimalField(max_digits=10, decimal_places=2)
    available = models.BooleanField(default=True)
    added_by_admin = models.ForeignKey(Admin, on_delete=models.CASCADE)
    added_date = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='cars/', null=True, blank=True)
    category = models.CharField(max_length=50, choices=[
        ('luxury', 'Luxury'),
        ('offroad', 'Offroad'),
        ('sedan', 'Sedan'),
        ('suv', 'SUV'),
        ('sports', 'Sports'),
    ], default='sedan')
    
    def __str__(self):
        return f"{self.year} {self.make} {self.model}"
    
    def set_unavailable(self):
        """Set the car as unavailable when booked"""
        self.available = False
        self.save()
    
    def set_available(self):
        """Set the car as available when booking is completed or cancelled"""
        self.available = True
        self.save()

class Booking(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
        ('completed', 'Completed'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    booking_date = models.DateField()
    return_date = models.DateField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='pending')
    created_by_admin = models.ForeignKey(Admin, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('user', 'car', 'booking_date')
    
    def __str__(self):
        return f"{self.user.username} - {self.car} ({self.booking_date} to {self.return_date})"

# Signal to update car availability when booking status changes
@receiver(post_save, sender=Booking)
def update_car_availability(sender, instance, created, **kwargs):
    if instance.status == 'confirmed':
        instance.car.set_unavailable()
    elif instance.status in ['cancelled', 'completed']:
        instance.car.set_available()

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    phone_number = models.CharField(max_length=15)
    profile_picture = models.ImageField(upload_to='profile_pics/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"

    class Meta:
        verbose_name = 'User Profile'
        verbose_name_plural = 'User Profiles'
