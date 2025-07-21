GOOGLE_GEOCODING_API_KEY="your_key_here"
GOOGLE_API_KEY = "api_key"

import os
import requests
from dotenv import load_dotenv

load_dotenv()

# GOOGLE_API_KEY = os.getenv("GOOGLE_GEOCODING_API_KEY")

def get_coordinates(location: str) -> tuple:
    url = f"https://maps.googleapis.com/maps/api/geocode/json?address={location}&key={GOOGLE_API_KEY}"
    response = requests.get(url)
    if response.status_code != 200:
        raise Exception("Google Geocoding API failed")
    data = response.json()
    if not data['results']:
        raise Exception("Location not found")

    loc = data['results'][0]['geometry']['location']
    return loc['lat'], loc['lng']


def get_weather_forecast(location: str) -> dict:
    lat, lon = get_coordinates(location)
    weather_url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current=temperature_2m,precipitation,wind_speed_10m"

    response = requests.get(weather_url)
    if response.status_code != 200:
        raise Exception("Weather API failed")

    data = response.json()
    current = data.get("current", {})

    return {
        "location": location,
        "temperature_C": current.get("temperature_2m"),
        "precipitation_mm": current.get("precipitation"),
        "wind_speed_kmh": current.get("wind_speed_10m"),
    }


def get_rainfall_data(location: str) -> float:
    forecast = get_weather_forecast(location)
    return forecast.get("precipitation_mm", 0.0)


def get_soil_moisture(location: str) -> float:
    # Placeholder: You can integrate NASA SMAP or similar APIs for real data
    return 0.21


def get_wind_speed(location: str) -> float:
    forecast = get_weather_forecast(location)
    return forecast.get("wind_speed_kmh", 0.0)


def get_temperature_range(location: str) -> tuple:
    lat, lon = get_coordinates(location)
    url = (
        f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}"
        f"&daily=temperature_2m_max,temperature_2m_min&timezone=auto"
    )
    response = requests.get(url)
    data = response.json()
    if "daily" not in data:
        return (None, None)

    return (
        data["daily"]["temperature_2m_min"][0],
        data["daily"]["temperature_2m_max"][0]
    )


# def get_weather_forecast(location: str) -> dict:
#     # Replace with actual API integration
#     return {
#         "location": location,
#         "forecast": "Partly cloudy with chances of rain"
#     }
#
# def get_rainfall_data(location: str) -> float:
#     return 12.4  # mm
#
# def get_soil_moisture(location: str) -> float:
#     return 0.25  # volumetric water content (m³/m³)
#
# def get_wind_speed(location: str) -> float:
#     return 14.2  # km/h
#
# def get_temperature_range(location: str) -> tuple:
#     return (18.0, 29.5)  # °C
