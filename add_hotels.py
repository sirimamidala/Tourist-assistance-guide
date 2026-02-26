from bookings.models import Service

hotels = [
    {"name": "Grand Plaza Hotel", "description": "Luxury stay with ocean view", "price_per_unit": 250.00, "contact": "+91 98765 43210"},
    {"name": "Sunset Resort", "description": "Perfect for families and relaxation", "price_per_unit": 180.00, "contact": "+91 87654 32109"},
    {"name": "City Center Inn", "description": "Affordable stay in the heart of the city", "price_per_unit": 90.00, "contact": "+91 76543 21098"},
    {"name": "Mountain View Lodge", "description": "Cozy cabin experience in the mountains", "price_per_unit": 150.00, "contact": "+91 65432 10987"},
    {"name": "Boutique Oasis", "description": "Unique decor and premium services", "price_per_unit": 210.00, "contact": "+91 54321 09876"},
]

for h in hotels:
    Service.objects.update_or_create(
        type='HOTEL',
        name=h['name'],
        defaults={
            'description': h['description'], 
            'price_per_unit': h['price_per_unit'],
            'contact_number': h['contact']
        }
    )

print("5 Hotels added successfully.")
