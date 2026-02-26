"""
Seed script to populate TouristPlace entries for the itinerary planner.
Run with: python manage.py shell < seed_tourist_places.py
or:       python seed_tourist_places.py
"""
import os
import sys
import django

# Setup Django
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tourist_project.settings')
django.setup()

from itinerary.models import TouristPlace

PLACES = [
    # TEMPLES - economy
    dict(name="Charminar", location="Hyderabad, Telangana", description="Iconic 16th-century mosque and monument, a symbol of Hyderabad with ornate arches and minarets.", interest_category="temples", budget_tier="economy", estimated_cost=50, image_url="https://upload.wikimedia.org/wikipedia/commons/thumb/4/44/New_Charminar.jpg/800px-New_Charminar.jpg"),
    dict(name="Birla Mandir", location="Hyderabad, Telangana", description="Stunning white marble temple dedicated to Lord Venkateswara, perched atop a rocky hill with panoramic views.", interest_category="temples", budget_tier="economy", estimated_cost=0, image_url="https://upload.wikimedia.org/wikipedia/commons/thumb/a/a7/Birla_Mandir%2C_Hyderabad%2C_India.jpg/800px-Birla_Mandir%2C_Hyderabad%2C_India.jpg"),
    dict(name="Thousand Pillar Temple", location="Warangal, Telangana", description="12th-century Kakatiya temple with intricately carved pillars dedicated to Shiva, Vishnu, and Surya.", interest_category="temples", budget_tier="economy", estimated_cost=30),
    dict(name="Ramappa Temple", location="Mulugu, Telangana", description="UNESCO World Heritage Site — a 13th-century Kakatiya masterpiece with floating bricks and exquisite sculptures.", interest_category="temples", budget_tier="economy", estimated_cost=50),
    dict(name="Yadadri Temple", location="Yadadri-Bhuvanagiri, Telangana", description="Ancient Narasimha Swamy temple recently renovated with gold-plated interiors on a rocky hilltop.", interest_category="temples", budget_tier="economy", estimated_cost=0),
    dict(name="Tirupati Balaji", location="Tirupati, Andhra Pradesh", description="One of the holiest and most visited pilgrimage sites in the world, dedicated to Lord Venkateswara.", interest_category="temples", budget_tier="moderate", estimated_cost=300),

    # ADVENTURE - moderate
    dict(name="Anegundi Coracle Ride", location="Hampi, Karnataka", description="Thrilling round coracle boat rides across the Tungabhadra river amidst stunning boulder landscapes.", interest_category="adventure", budget_tier="moderate", estimated_cost=500),
    dict(name="Bhongir Rock Climbing", location="Bhongir, Telangana", description="Exciting rock climbing and trekking on the historic single-rock fort of Bhongir.", interest_category="adventure", budget_tier="economy", estimated_cost=100),
    dict(name="Kundala Lake Boating", location="Munnar, Kerala", description="Serene boating on the high-altitude Kundala Lake surrounded by misty tea gardens and dam scenery.", interest_category="adventure", budget_tier="moderate", estimated_cost=400),
    dict(name="Dudhsagar Waterfall Trek", location="Goa/Karnataka border", description="Adventurous jungle trek to the magnificent four-tiered Dudhsagar Falls, one of India's tallest.", interest_category="adventure", budget_tier="moderate", estimated_cost=600),
    dict(name="Bungee Jumping at Wanderlust", location="Rishikesh, Uttarakhand", description="India's highest bungee jump at 83m, set over the Ganges with breathtaking Himalayan views.", interest_category="adventure", budget_tier="luxury", estimated_cost=3500),
    dict(name="River Rafting Rishikesh", location="Rishikesh, Uttarakhand", description="White-water rafting through Grade III-V rapids on the holy Ganges river — an unforgettable rush.", interest_category="adventure", budget_tier="moderate", estimated_cost=800),

    # HILL STATIONS - moderate
    dict(name="Araku Valley", location="Visakhapatnam, Andhra Pradesh", description="Scenic hill station known for coffee plantations, waterfalls, tribal culture, and cool breezy weather.", interest_category="hill_stations", budget_tier="moderate", estimated_cost=800, image_url="https://upload.wikimedia.org/wikipedia/commons/thumb/9/9b/Araku_Valley.jpg/800px-Araku_Valley.jpg"),
    dict(name="Horsley Hills", location="Andhra Pradesh", description="Tranquil hill station at 1265m, offering panoramic views, eucalyptus forests, and a cool climate.", interest_category="hill_stations", budget_tier="economy", estimated_cost=300),
    dict(name="Munnar", location="Idukki, Kerala", description="Stunning hill station blanketed with sprawling tea gardens, misty peaks, and waterfalls.", interest_category="hill_stations", budget_tier="moderate", estimated_cost=1200, image_url="https://upload.wikimedia.org/wikipedia/commons/thumb/0/00/Munnar%2C_Kerala_%281%29.jpg/800px-Munnar%2C_Kerala_%281%29.jpg"),
    dict(name="Ooty", location="Nilgiris, Tamil Nadu", description="The 'Queen of Hill Stations' — known for its botanical garden, toy train, and rolling tea estates.", interest_category="hill_stations", budget_tier="moderate", estimated_cost=1000),
    dict(name="Manali", location="Himachal Pradesh", description="Popular Himalayan hill station with adventure sports, ancient temples, and spectacular mountain views.", interest_category="hill_stations", budget_tier="moderate", estimated_cost=1500),
    dict(name="Coorg", location="Karnataka", description="Scotland of India — lush coffee estates, mist-covered mountains, orange orchards, and cascading waterfalls.", interest_category="hill_stations", budget_tier="moderate", estimated_cost=1200),

    # FOOD - economy  
    dict(name="Paradise Restaurant", location="Secunderabad, Hyderabad", description="Legendary dum biryani restaurant serving the iconic Hyderabadi Dum Biryani since 1953.", interest_category="food", budget_tier="moderate", estimated_cost=400),
    dict(name="Haleem Food Street", location="Tolichowki, Hyderabad", description="Famous Ramadan-special lane of restaurants serving world-class Hyderabadi Haleem, awarded GI tag.", interest_category="food", budget_tier="economy", estimated_cost=200),
    dict(name="Street Food Trail - Charminar", location="Old City, Hyderabad", description="Vibrant street food trail with Irani chai, Osmania biscuits, double ka meetha, and kebabs.", interest_category="food", budget_tier="economy", estimated_cost=150),
    dict(name="Saravana Bhavan", location="Chennai, Tamil Nadu", description="World-famous South Indian vegetarian restaurant chain known for crispy dosas, idlis, and filter coffee.", interest_category="food", budget_tier="economy", estimated_cost=250),
    dict(name="Goa Beach Shacks", location="Calangute, Goa", description="Iconic Goan beachside shacks serving fresh seafood, fish curry rice, and exotic cocktails.", interest_category="food", budget_tier="moderate", estimated_cost=700),
    dict(name="Mumbai Vada Pav Trail", location="Mumbai, Maharashtra", description="Iconic street food trail across Dadar and Girgaon tasting Mumbai's beloved Vada Pav and Pav Bhaji.", interest_category="food", budget_tier="economy", estimated_cost=100),

    # SHOPPING - moderate
    dict(name="Laad Bazaar", location="Hyderabad, Telangana", description="350-year-old market near Charminar famous for bangles, pearls, silver jewellery, and bridal wear.", interest_category="shopping", budget_tier="moderate", estimated_cost=500),
    dict(name="Janpath Market", location="New Delhi", description="Popular open-air flea market on Janpath road with handicrafts, textiles, jewellery, and antiques.", interest_category="shopping", budget_tier="economy", estimated_cost=300),
    dict(name="Dilli Haat", location="New Delhi", description="Open-air craft village showcasing handlooms, handicrafts, and cuisines from 29 Indian states.", interest_category="shopping", budget_tier="moderate", estimated_cost=400),
    dict(name="Commercial Street", location="Bengaluru, Karnataka", description="Bengaluru's premier shopping destination for clothing, accessories, street food, and everything trendy.", interest_category="shopping", budget_tier="moderate", estimated_cost=600),
    dict(name="Tibetan Market", location="Rishikesh, Uttarakhand", description="Colourful Tibetan market with handcrafted jewellery, woollen shawls, Buddhist artefacts, and incense.", interest_category="shopping", budget_tier="economy", estimated_cost=400),

    # BEACHES - economy
    dict(name="Rushikonda Beach", location="Visakhapatnam, Andhra Pradesh", description="Clean golden-sand beach with water sports, backed by green hills — the 'Jewel of East Coast'.", interest_category="beaches", budget_tier="economy", estimated_cost=200, image_url="https://upload.wikimedia.org/wikipedia/commons/thumb/a/a4/Rushikonda_beach.jpg/800px-Rushikonda_beach.jpg"),
    dict(name="Calangute Beach", location="Goa", description="The 'Queen of Beaches' in Goa, lively with water sports, beach shacks, and vibrant nightlife.", interest_category="beaches", budget_tier="moderate", estimated_cost=800),
    dict(name="Radhanagar Beach", location="Andaman Islands", description="One of Asia's best beaches — pristine white sands, turquoise waters, and spectacular sunsets.", interest_category="beaches", budget_tier="luxury", estimated_cost=2000),
    dict(name="Kovalam Beach", location="Thiruvananthapuram, Kerala", description="Crescent-shaped beach famous for Ayurvedic resorts, lighthouse views, and surfing.", interest_category="beaches", budget_tier="moderate", estimated_cost=700),
    dict(name="Marina Beach", location="Chennai, Tamil Nadu", description="World's second-longest urban beach, bustling with street food, horse rides, and evening promenades.", interest_category="beaches", budget_tier="economy", estimated_cost=50),

    # HISTORICAL - moderate
    dict(name="Golconda Fort", location="Hyderabad, Telangana", description="Magnificent 400-year-old fort of the Qutb Shahi dynasty with iconic acoustics and panoramic views.", interest_category="historical", budget_tier="economy", estimated_cost=100, image_url="https://upload.wikimedia.org/wikipedia/commons/thumb/b/b6/Golkonda_fort_Hyderabad.jpg/800px-Golkonda_fort_Hyderabad.jpg"),
    dict(name="Red Fort", location="New Delhi", description="Iconic Mughal fort and UNESCO World Heritage Site, the symbol of India's sovereignty.", interest_category="historical", budget_tier="economy", estimated_cost=200),
    dict(name="Qutb Minar", location="New Delhi", description="World's tallest brick minaret (73m), a UNESCO World Heritage Site of the Delhi Sultanate era.", interest_category="historical", budget_tier="economy", estimated_cost=200),
    dict(name="Hampi Ruins", location="Hampi, Karnataka", description="Sprawling UNESCO World Heritage Site — ruins of the Vijayanagara Empire amid surreal boulder landscapes.", interest_category="historical", budget_tier="economy", estimated_cost=300),
    dict(name="Taj Mahal", location="Agra, Uttar Pradesh", description="One of the Seven Wonders of the World — the ultimate symbol of love built by Shah Jahan.", interest_category="historical", budget_tier="moderate", estimated_cost=1100),

    # NATURE - economy
    dict(name="Nagarjuna Sagar Wildlife Sanctuary", location="Andhra Pradesh", description="Core habitat for tigers, leopards, and rare animals in a protected biosphere reserve.", interest_category="nature", budget_tier="moderate", estimated_cost=600),
    dict(name="Mrugavani National Park", location="Hyderabad, Telangana", description="Green lung near Hyderabad — nature trails, rare birds, and a mini-zoo in a serene setting.", interest_category="nature", budget_tier="economy", estimated_cost=50),
    dict(name="Periyar Wildlife Sanctuary", location="Thekkady, Kerala", description="Famous for boat safaris on Periyar Lake with sightings of elephants, tigers, and rare birds.", interest_category="nature", budget_tier="moderate", estimated_cost=800),
    dict(name="Jim Corbett National Park", location="Uttarakhand", description="India's oldest national park and premier tiger reserve with dense forests and rich biodiversity.", interest_category="nature", budget_tier="luxury", estimated_cost=3000),
    dict(name="Chilika Lake", location="Odisha", description="Asia's largest brackish water lagoon — famous for irrawaddy dolphins and migratory flamingos.", interest_category="nature", budget_tier="economy", estimated_cost=300),
]


def run():
    created = 0
    skipped = 0
    for data in PLACES:
        obj, was_created = TouristPlace.objects.get_or_create(
            name=data['name'],
            location=data['location'],
            defaults={k: v for k, v in data.items() if k not in ('name', 'location')}
        )
        if was_created:
            created += 1
        else:
            skipped += 1

    print(f"✅ Done! {created} places created, {skipped} already existed.")
    print(f"   Total TouristPlaces in DB: {TouristPlace.objects.count()}")


if __name__ == '__main__':
    run()
