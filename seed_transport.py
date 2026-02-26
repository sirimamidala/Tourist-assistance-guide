from bookings.models import Service

transport_services = [
    {
        "name": "City Express Taxi",
        "description": "Fast and reliable city taxis available 24/7.",
        "price_per_unit": 15.00,
        "transport_category": "CAB",
        "pickup_location": "Anywhere in City Limits",
        "contact_number": "+1-555-0101",
        "rating": 4.5
    },
    {
        "name": "Prime Luxury Cabs",
        "description": "Premium chauffeur-driven cars for ultimate comfort.",
        "price_per_unit": 45.00,
        "transport_category": "CAB",
        "pickup_location": "Airport & Major Hotels",
        "contact_number": "+1-555-0102",
        "rating": 4.9
    },
    {
        "name": "Metro Transit Bus",
        "description": "City-wide bus network, affordable and eco-friendly.",
        "price_per_unit": 2.50,
        "transport_category": "BUS",
        "pickup_location": "Central Bus Station",
        "contact_number": "+1-555-0201",
        "rating": 4.2
    },
    {
        "name": "Intercity Coaches",
        "description": "Comfortable AC buses for long-distance travel.",
        "price_per_unit": 35.00,
        "transport_category": "BUS",
        "pickup_location": "North Terminal",
        "contact_number": "+1-555-0202",
        "rating": 4.6
    },
    {
        "name": "Regional Rail",
        "description": "Quick trains connecting neighboring towns.",
        "price_per_unit": 12.00,
        "transport_category": "TRAIN",
        "pickup_location": "Central Station",
        "contact_number": "+1-555-0301",
        "rating": 4.4
    },
    {
        "name": "SkyHigh Airlines",
        "description": "Domestic flights with excellent on-time performance.",
        "price_per_unit": 150.00,
        "transport_category": "FLIGHT",
        "pickup_location": "International Airport",
        "contact_number": "+1-555-0401",
        "rating": 4.7
    },
    {
        "name": "Freedom Car Rentals",
        "description": "Self-drive cars ranging from hatchbacks to SUVs.",
        "price_per_unit": 60.00,
        "transport_category": "CAR_RENTAL",
        "pickup_location": "City Center Depot",
        "contact_number": "+1-555-0501",
        "rating": 4.8
    },
    {
        "name": "Zip Scooters",
        "description": "Easy to ride scooters for navigating local streets.",
        "price_per_unit": 10.00,
        "transport_category": "BIKE_RENTAL",
        "pickup_location": "Multiple City Hubs",
        "contact_number": "+1-555-0601",
        "rating": 4.3
    }
]

for t in transport_services:
    Service.objects.get_or_create(
        type='TRANSPORT',
        name=t['name'],
        defaults={
            'description': t['description'], 
            'price_per_unit': t['price_per_unit'],
            'transport_category': t['transport_category'],
            'pickup_location': t['pickup_location'],
            'contact_number': t['contact_number'],
            'rating': t['rating']
        }
    )

print("8 Transport Services added successfully.")
