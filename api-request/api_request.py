import os
import requests


API_KEY = os.getenv("WEATHERSTACK_API_KEY")
CITY = os.getenv("WEATHER_CITY", "New York")
API_URL = f"http://api.weatherstack.com/current?access_key={API_KEY}&query={CITY}"


def feath_data():
    if not API_KEY:
        raise RuntimeError(
            "WEATHERSTACK_API_KEY is not set. "
            "Add it to your .env file or container environment."
        )
    response = requests.get(API_URL)
    return response.json()


def mock_fetch_data():
    return {'request': {'type': 'City', 'query': 'New York, United States of America', 'language': 'en', 'unit': 'm'}, 'location': {'name': 'New York', 'country': 'United States of America', 'region': 'New York', 'lat': '40.714', 'lon': '-74.006', 'timezone_id': 'America/New_York', 'localtime': '2026-04-23 10:04', 'localtime_epoch': 1776938640, 'utc_offset': '-4.0'}, 'current': {'observation_time': '02:04 PM', 'temperature': 12, 'weather_code': 113, 'weather_icons': ['https://cdn.worldweatheronline.com/images/wsymbols01_png_64/wsymbol_0001_sunny.png'], 'weather_descriptions': ['Sunny'], 'astro': {'sunrise': '06:05 AM', 'sunset': '07:44 PM', 'moonrise': '11:22 AM', 'moonset': '02:03 AM', 'moon_phase': 'Waxing Crescent', 'moon_illumination': 38}, 'air_quality': {'co': '185.85', 'no2': '5.55', 'o3': '115', 'so2': '3.85', 'pm2_5': '8.05', 'pm10': '9.25', 'us-epa-index': '1', 'gb-defra-index': '1'}, 'wind_speed': 8, 'wind_degree': 290, 'wind_dir': 'WNW', 'pressure': 1016, 'precip': 0, 'humidity': 74, 'cloudcover': 0, 'feelslike': 11, 'uv_index': 3, 'visibility': 13, 'is_day': 'yes'}}
