def get_weather_forecast(location: str) -> dict:
    # Replace with actual API integration
    return {
        "location": location,
        "forecast": "Partly cloudy with chances of rain"
    }

def get_rainfall_data(location: str) -> float:
    return 12.4  # mm

def get_soil_moisture(location: str) -> float:
    return 0.25  # volumetric water content (m³/m³)

def get_wind_speed(location: str) -> float:
    return 14.2  # km/h

def get_temperature_range(location: str) -> tuple:
    return (18.0, 29.5)  # °C
