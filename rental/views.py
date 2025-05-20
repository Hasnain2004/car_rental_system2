from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from datetime import datetime, timedelta
from decimal import Decimal
from .models import Car, Booking, Admin
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.decorators import user_passes_test

def is_guest(user):
    return not user.is_authenticated

@login_required(login_url='rental:login')
def car_list(request):
    cars = Car.objects.filter(available=True)
    categories = Car.objects.values_list('category', flat=True).distinct()
    context = {
        'cars': cars,
        'categories': categories
    }
    return render(request, 'rental/car_list.html', context)

@login_required(login_url='rental:login')
def car_filter(request, category):
    cars = Car.objects.filter(available=True, category=category)
    categories = Car.objects.values_list('category', flat=True).distinct()
    context = {
        'cars': cars,
        'categories': categories,
        'current_category': category
    }
    return render(request, 'rental/car_list.html', context)

@login_required(login_url='rental:login')
def car_detail(request, car_id):
    car = get_object_or_404(Car, id=car_id)
    context = {
        'car': car
    }
    return render(request, 'rental/car_detail.html', context)

def home(request):
    featured_cars = Car.objects.filter(available=True).order_by('-added_date')[:3]
    categories = Car.objects.values_list('category', flat=True).distinct()
    context = {
        'featured_cars': featured_cars,
        'categories': categories,
        'show_signup': not request.user.is_authenticated
    }
    return render(request, 'rental/home.html', context)

@login_required
def book_car(request, car_id):
    car = get_object_or_404(Car, id=car_id)
    
    if request.method == 'POST':
        booking_date = request.POST.get('booking_date')
        return_date = request.POST.get('return_date')
        
        # Validate dates
        booking_date = datetime.strptime(booking_date, '%Y-%m-%d').date()
        return_date = datetime.strptime(return_date, '%Y-%m-%d').date()
        
        if booking_date < datetime.now().date():
            messages.error(request, "Booking date cannot be in the past")
            return redirect('rental:car_detail', car_id=car.id)
            
        if return_date <= booking_date:
            messages.error(request, "Return date must be after booking date")
            return redirect('rental:car_detail', car_id=car.id)
        
        # Calculate number of days
        days = (return_date - booking_date).days
        total_price = car.price_per_day * Decimal(days)
        
        # Get the first admin (this is just a placeholder - in a real system we'd have better logic)
        admin = Admin.objects.first()
        
        # Create booking
        booking = Booking(
            user=request.user,
            car=car,
            booking_date=booking_date,
            return_date=return_date,
            total_price=total_price,
            created_by_admin=admin
        )
        booking.save()
        
        messages.success(request, "Booking request submitted successfully. Waiting for admin approval.")
        return redirect('rental:my_bookings')
    
    context = {
        'car': car,
        'min_date': datetime.now().date(),
        'min_return_date': datetime.now().date() + timedelta(days=1)
    }
    return render(request, 'rental/book_car.html', context)

@login_required
def my_bookings(request):
    bookings = Booking.objects.filter(user=request.user).order_by('-created_at')
    context = {
        'bookings': bookings
    }
    return render(request, 'rental/my_bookings.html', context)

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('rental:home')
    else:
        form = UserCreationForm()
    return render(request, 'rental/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('rental:home')
    else:
        form = AuthenticationForm()
    return render(request, 'rental/login.html', {'form': form})

@login_required
def logout_view(request):
    logout(request)
    return redirect('rental:home')

def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        
        # Here you would typically send an email
        # For now, we'll just show a success message
        messages.success(request, "Thank you for your message. We'll get back to you soon!")
        return redirect('rental:contact')
    
    return render(request, 'rental/contact.html')

def about(request):
    return render(request, 'rental/about.html')
