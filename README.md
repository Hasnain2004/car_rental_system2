# LuxDrive Car Rental System

A premium car rental web application built with Django. This application allows users to browse, filter, and book luxury, sports, sedan, SUV, and off-road vehicles.

## Features

- **User Authentication**: Register, login, and manage your account
- **Car Browsing**: View all available cars with detailed information
- **Category Filtering**: Filter cars by category (Luxury, Sports, Sedan, SUV, Off-road)
- **Booking System**: Book cars for specific dates with automatic price calculation
- **Booking Management**: View and manage your bookings
- **Admin Approval**: Bookings require admin approval before confirmation
- **Responsive Design**: Fully responsive design works on all devices

## Technologies Used

- Django 5.2
- Bootstrap 5
- JavaScript
- HTML/CSS
- SQLite (can be configured for PostgreSQL)

## Installation

1. Clone the repository

```
git clone https://github.com/yourusername/car_rental_system.git
cd car_rental_system
```

2. Create and activate a virtual environment

```
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies

```
pip install -r requirements.txt
```

4. Run migrations

```
python manage.py migrate
```

5. Create a superuser (for admin access)

```
python manage.py createsuperuser
```

6. Load sample data (optional)

```
python sample_data.py
```

7. Run the development server

```
python manage.py runserver
```

8. Access the site at `http://127.0.0.1:8000`

## Usage

### For Users

1. Register a new account or login with existing credentials
2. Browse available cars or filter by category
3. Select a car and view its details
4. Choose booking dates and submit a booking request
5. View your bookings in the "My Bookings" section
6. Wait for admin approval of your booking

### For Admins

1. Login to the admin panel at `http://127.0.0.1:8000/admin`
2. Manage cars (add, edit, delete)
3. Review and approve booking requests
4. Update booking status (confirm, cancel, complete)

## Project Structure

- `rental/` - Main app directory
  - `models.py` - Database models (Admin, Car, Booking)
  - `views.py` - View functions for handling requests
  - `urls.py` - URL routing for the app
  - `admin.py` - Admin panel configuration
  - `templates/` - HTML templates
  - `static/` - CSS, JS, and image files

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
