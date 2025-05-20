import os
import django
from datetime import datetime
import random

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'car_rental_system.settings')
django.setup()

# Import models after Django setup
from rental.models import Admin, Car

# Create admin user
def create_admin():
    try:
        admin = Admin.objects.get(username='carsadmin')
        print("Admin user already exists!")
    except Admin.DoesNotExist:
        admin = Admin(
            username='carsadmin',
            password='carsadmin123',
            last_login=datetime.now()
        )
        admin.save()
        print("Admin user 'carsadmin' created successfully!")
    return admin

# Create sample cars
def create_cars(admin):
    # Sample car data
    cars = [
        {
            'make': 'BMW',
            'model': 'X5',
            'year': 2023,
            'price_per_day': 150.00,
            'category': 'luxury'
        },
        {
            'make': 'Toyota',
            'model': 'Camry',
            'year': 2022,
            'price_per_day': 80.00,
            'category': 'sedan'
        },
        {
            'make': 'Honda',
            'model': 'Civic',
            'year': 2023,
            'price_per_day': 75.00,
            'category': 'sedan'
        },
        {
            'make': 'Jeep',
            'model': 'Wrangler',
            'year': 2022,
            'price_per_day': 120.00,
            'category': 'offroad'
        },
        {
            'make': 'Ford',
            'model': 'Explorer',
            'year': 2023,
            'price_per_day': 100.00,
            'category': 'suv'
        },
        {
            'make': 'Mercedes-Benz',
            'model': 'S-Class',
            'year': 2023,
            'price_per_day': 200.00,
            'category': 'luxury'
        },
        {
            'make': 'Porsche',
            'model': '911',
            'year': 2023,
            'price_per_day': 250.00,
            'category': 'sports'
        },
        {
            'make': 'Toyota',
            'model': 'Land Cruiser',
            'year': 2022,
            'price_per_day': 150.00,
            'category': 'offroad'
        },
        {
            'make': 'Ferrari',
            'model': 'F8 Tributo',
            'year': 2023,
            'price_per_day': 300.00,
            'category': 'sports'
        }
    ]
    
    cars_created = 0
    for car_data in cars:
        if not Car.objects.filter(make=car_data['make'], model=car_data['model'], year=car_data['year']).exists():
            car = Car(
                make=car_data['make'],
                model=car_data['model'],
                year=car_data['year'],
                price_per_day=car_data['price_per_day'],
                available=True,
                added_by_admin=admin,
                category=car_data['category']
            )
            car.save()
            cars_created += 1
    
    print(f"{cars_created} new cars added successfully!")

if __name__ == "__main__":
    admin = create_admin()
    create_cars(admin)
    print("Sample data created successfully!") 