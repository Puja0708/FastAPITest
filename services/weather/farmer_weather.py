from weather_utils import *

def get_all_weather_data(location: str):
    return {
        "forecast": get_weather_forecast(location),
        "rainfall": get_rainfall_data(location),
        "soil_moisture": get_soil_moisture(location),
        "wind_speed": get_wind_speed(location),
        "temperature_range": get_temperature_range(location),
    }
