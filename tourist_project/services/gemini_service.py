import os
import google.generativeai as genai
from django.conf import settings

class GeminiService:
    """
    Service helper for AI Travel Planning using Google Gemini.
    """
    @staticmethod
    def generate_itinerary(destination, days, interests):
        api_key = getattr(settings, "GEMINI_API_KEY", None)
        if not api_key:
            return "AI Planner is currently in mock mode. (API Key missing)"

        try:
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel('gemini-pro')
            prompt = f"Create a detailed {days}-day travel itinerary for {destination} focusing on {interests}. Format as a structured list."
            response = model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"Error generating itinerary: {str(e)}"

    @staticmethod
    def find_global_places(query):
        api_key = getattr(settings, "GEMINI_API_KEY", None)
        if not api_key:
            return []

        try:
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel('gemini-pro')
            prompt = (
                f"Act as a travel expert. Find 5 real-world tourist places related to the search query: '{query}'. "
                "For each place, provide a JSON-like structured list with: "
                "'name', 'location', 'description' (short), and 'category' (one of: BEACH, HILL_STATION, HISTORICAL, NATURE, ADVENTURE, CITY, OTHER). "
                "Output ONLY the raw data in a simple format that can be easily parsed (Pipe separated: Name|Location|Description|Category). "
                "Ensure each place is on a new line."
            )
            response = model.generate_content(prompt)
            lines = response.text.strip().split('\n')
            places = []
            for line in lines:
                parts = line.split('|')
                if len(parts) >= 4:
                    places.append({
                        'name': parts[0].strip(),
                        'location': parts[1].strip(),
                        'description': parts[2].strip(),
                        'category': parts[3].strip()
                    })
            return places
        except Exception as e:
            print(f"Error searching global places: {str(e)}")
            return []
