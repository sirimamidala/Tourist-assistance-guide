import requests
from django.conf import settings

class WeatherService:
    """
    Service helper to fetch real-time weather data.
    """
    API_URL = "https://api.openweathermap.org/data/2.5/weather"

    @staticmethod
    def get_weather(location):
        api_key = getattr(settings, "OPENWEATHER_API_KEY", None)
        if not api_key:
            return {"error": "API Key missing", "temp": "N/A", "condition": "Unknown"}

        try:
            params = {
                "q": location,
                "appid": api_key,
                "units": "metric"
            }
            response = requests.get(WeatherService.API_URL, params=params)
            data = response.json()
            if response.status_code == 200:
                return {
                    "temp": data["main"]["temp"],
                    "condition": data["weather"][0]["main"],
                    "description": data["weather"][0]["description"],
                    "icon": data["weather"][0]["icon"]
                }
            return {"error": data.get("message", "Error fetching weather")}
        except Exception as e:
            return {"error": str(e)}
