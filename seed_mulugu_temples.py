"""
Seed script for Mulugu region temples and attractions.
"""
import os
import sys
import django

# Setup Django
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tourist_project.settings')
django.setup()

from itinerary.models import TouristPlace

MULUGU_PLACES = [
    dict(
        name="Medaram Sammakka Saralamma Temple",
        location="Mulugu, Telangana",
        description="Site of the largest tribal congregation in the world, dedicated to the folk goddesses Sammakka and Saralamma.",
        interest_category="temples",
        budget_tier="economy",
        estimated_cost=0
    ),
    dict(
        name="Mallur Hemachala Lakshmi Narasimha Swamy",
        location="Mulugu, Telangana",
        description="An ancient temple on a hill known for its continuous water flow from the idol's feet and medicinal herbs in the surrounding forest.",
        interest_category="temples",
        budget_tier="economy",
        estimated_cost=50
    ),
    dict(
        name="Bogatha Waterfall",
        location="Mulugu, Telangana",
        description="Known as the 'Niagara of Telangana', a beautiful waterfall surrounded by lush forests — great for a day trip from the temples.",
        interest_category="nature",
        budget_tier="economy",
        estimated_cost=100
    ),
    dict(
        name="Laknavaram Lake",
        location="Govindaraopet, Mulugu",
        description="A massive scenic lake with 13 islands and a famous hanging bridge, offering boating and serene views.",
        interest_category="nature",
        budget_tier="moderate",
        estimated_cost=300
    ),
    dict(
        name="Tadvai Huts & Safari",
        location="Eturnagaram, Mulugu",
        description="Eco-tourism destination offering night camping in forest huts and wildlife safari in the Eturnagaram Wildlife Sanctuary.",
        interest_category="adventure",
        budget_tier="moderate",
        estimated_cost=1500
    ),
]

def run():
    created = 0
    skipped = 0
    for data in MULUGU_PLACES:
        obj, was_created = TouristPlace.objects.get_or_create(
            name=data['name'],
            location=data['location'],
            defaults={k: v for k, v in data.items() if k not in ('name', 'location')}
        )
        if was_created:
            created += 1
        else:
            skipped += 1

    print(f"✅ Success! {created} Mulugu region places added, {skipped} already existed.")
    print(f"   Current total places in system: {TouristPlace.objects.count()}")

if __name__ == '__main__':
    run()
