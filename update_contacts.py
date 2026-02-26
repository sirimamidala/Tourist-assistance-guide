import random

# Update all services with unique 10-digit numbers
services = Service.objects.all()
for service in services:
    # Generate a random 10-digit number
    # Starting with 7, 8, or 9 for realism
    contact = f"{random.randint(7, 9)}{random.randint(0, 999999999):09d}"
    service.contact_number = contact
    service.save()

print(f"Updated {services.count()} services with unique 10-digit contact numbers.")
