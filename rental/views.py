from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from datetime import datetime, timedelta
from decimal import Decimal
from .models import Car, Booking, Admin, UserProfile, ContactMessage
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.decorators import user_passes_test
from .forms import CustomUserCreationForm

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
    if request.user.is_staff:
        # For admin users, show all pending booking requests
        bookings = Booking.objects.filter(status='pending').order_by('-created_at')
        template = 'rental/booking_requests.html'
        context = {
            'bookings': bookings,
            'is_admin': True
        }
    else:
        # For regular users, show their own bookings
        bookings = Booking.objects.filter(user=request.user).order_by('-created_at')
        template = 'rental/my_bookings.html'
        context = {
            'bookings': bookings,
            'is_admin': False
        }
    return render(request, template, context)

@login_required
def update_booking_status(request, booking_id):
    if not request.user.is_staff:
        messages.error(request, "You don't have permission to perform this action.")
        return redirect('rental:my_bookings')
    
    try:
        booking = Booking.objects.get(id=booking_id)
        new_status = request.POST.get('status')
        
        if new_status in ['confirmed', 'cancelled']:
            booking.status = new_status
            booking.save()
            
            # Send email notification to the user
            subject = f"Booking {new_status.title()} - LuxDrive Rentals"
            message = f"""
            Dear {booking.user.get_full_name()},
            
            Your booking request for {booking.car} has been {new_status}.
            
            Booking Details:
            - Booking Date: {booking.booking_date}
            - Return Date: {booking.return_date}
            - Total Price: ${booking.total_price}
            
            {f"Thank you for choosing LuxDrive Rentals. We look forward to serving you!" if new_status == 'confirmed' else "We apologize for any inconvenience. Please feel free to contact us if you have any questions."}
            
            Best regards,
            LuxDrive Rentals Team
            """
            
            booking.user.email_user(subject, message)
            
            messages.success(request, f"Booking has been {new_status} successfully.")
        else:
            messages.error(request, "Invalid status provided.")
            
    except Booking.DoesNotExist:
        messages.error(request, "Booking not found.")
    except Exception as e:
        messages.error(request, f"An error occurred: {str(e)}")
    
    return redirect('rental:my_bookings')

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            
            # Create user profile with phone number only
            UserProfile.objects.create(
                user=user,
                phone_number=form.cleaned_data.get('phone_number')
            )
            
            # Send welcome email
            try:
                send_mail(
                    'Welcome to LuxDrive Rentals!',
                    f'Dear {user.first_name},\n\nWelcome to LuxDrive Rentals! We are excited to have you as a member.\n\n'
                    'You can now browse our car collection and make bookings.\n\n'
                    'Best regards,\nLuxDrive Rentals Team',
                    settings.DEFAULT_FROM_EMAIL,
                    [user.email],
                    fail_silently=True,
                )
            except:
                pass  # Email sending is optional
            
            login(request, user)
            messages.success(request, "Registration successful! Welcome to LuxDrive Rentals.")
            return redirect('rental:home')
    else:
        form = CustomUserCreationForm()
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
        
        # Save the message to database
        ContactMessage.objects.create(
            name=name,
            email=email,
            subject=subject,
            message=message
        )
        
        # Send email notification to admin (optional)
        try:
            admin_email = settings.ADMIN_EMAIL if hasattr(settings, 'ADMIN_EMAIL') else settings.DEFAULT_FROM_EMAIL
            send_mail(
                f'New Contact Message: {subject}',
                f'Name: {name}\nEmail: {email}\n\nMessage:\n{message}',
                settings.DEFAULT_FROM_EMAIL,
                [admin_email],
                fail_silently=True,
            )
        except:
            pass  # Email sending is optional
        
        messages.success(request, "Thank you for your message. We'll get back to you soon!")
        return redirect('rental:contact')
    
    return render(request, 'rental/contact.html')

def about(request):
    return render(request, 'rental/about.html')
