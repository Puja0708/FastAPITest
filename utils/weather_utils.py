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
    """
    Get estimated soil moisture data for a given location using Open-Meteo API.

    Args:
        location (str): Name of the location (e.g., "New Delhi, India").

    Returns:
        float: Soil moisture value (m3/m3) or -1.0 if not found.
    """
    try:
        # Step 1: Geocode the location
        geo_url = "https://nominatim.openstreetmap.org/search"
        geo_params = {"q": location, "format": "json", "limit": 1}
        geo_res = requests.get(geo_url, params=geo_params, timeout=10)
        geo_res.raise_for_status()
        geo_data = geo_res.json()
        if not geo_data:
            return -1.0
        lat, lon = geo_data[0]["lat"], geo_data[0]["lon"]

        # Step 2: Query Open-Meteo for soil moisture
        soil_url = "https://api.open-meteo.com/v1/forecast"
        soil_params = {
            "latitude": lat,
            "longitude": lon,
            "hourly": "soil_moisture_0_1cm",
            "forecast_days": 1,
            "timezone": "auto"
        }
        soil_res = requests.get(soil_url, params=soil_params, timeout=10)
        soil_res.raise_for_status()
        soil_data = soil_res.json()

        moisture = soil_data.get("hourly", {}).get("soil_moisture_0_1cm", [])
        return float(moisture[0]) if moisture else -1.0

    except Exception as e:
        print(f"Error fetching soil moisture: {e}")
        return -1.0


# def get_soil_moisture(location: str) -> float:
#     # Placeholder: You can integrate NASA SMAP or similar APIs for real data
#     return 0.21


def get_wind_speed(location: str) -> float:
    forecast = get_weather_forecast(location)
    return forecast.get("wind_speed_kmh", 0.0)

def get_lat_lon(location: str, api_key: str) -> tuple:
    url = "https://maps.googleapis.com/maps/api/geocode/json"
    params = {"address": location, "key": api_key}
    response = requests.get(url, params=params).json()
    if response["status"] == "OK":
        loc = response["results"][0]["geometry"]["location"]
        return loc["lat"], loc["lng"]
    return (None, None)



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
