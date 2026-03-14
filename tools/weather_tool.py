# tools/weather_tool.py
"""
Professional weather tool with caching and enhanced error handling
"""

import requests
import time
from typing import Dict, Optional

# Simple in-memory cache
_weather_cache = {}
_CACHE_DURATION = 1800  # 30 minutes

def get_weather(lat: float, lon: float, use_cache: bool = True) -> Dict:
    """
    Get current weather information for given GPS coordinates.

    Args:
        lat: Latitude (-90 to 90)
        lon: Longitude (-180 to 180)
        use_cache: Whether to use cached results

    Returns:
        Dictionary with weather information or error details
    """

    # Validate coordinates
    if not (-90 <= lat <= 90):
        return {"error": "Invalid latitude. Must be between -90 and 90."}

    if not (-180 <= lon <= 180):
        return {"error": "Invalid longitude. Must be between -180 and 180."}

    # Check cache
    cache_key = f"{lat:.4f},{lon:.4f}"
    if use_cache and cache_key in _weather_cache:
        cached_data, timestamp = _weather_cache[cache_key]
        if time.time() - timestamp < _CACHE_DURATION:
            return cached_data

    # API call to Open-Meteo (free, no API key required)
    url = (
        "https://api.open-meteo.com/v1/forecast"
        f"?latitude={lat}&longitude={lon}"
        "&current_weather=true"
        "&timezone=Asia/Ho_Chi_Minh"
    )

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()

        data = response.json()

        if "current_weather" not in data:
            return {"error": "Weather data not available for this location."}

        current = data["current_weather"]

        # Format the response
        result = {
            "temperature": current.get("temperature"),
            "temperature_unit": "°C",
            "windspeed": current.get("windspeed"),
            "windspeed_unit": "km/h",
            "winddirection": current.get("winddirection"),
            "winddirection_unit": "°",
            "weathercode": current.get("weathercode"),
            "time": current.get("time"),
            "coordinates": {"lat": lat, "lon": lon}
        }

        # Add weather description based on WMO code
        weather_descriptions = {
            0: "Clear sky",
            1: "Mainly clear", 2: "Partly cloudy", 3: "Overcast",
            45: "Fog", 48: "Depositing rime fog",
            51: "Light drizzle", 53: "Moderate drizzle", 55: "Dense drizzle",
            56: "Light freezing drizzle", 57: "Dense freezing drizzle",
            61: "Slight rain", 63: "Moderate rain", 65: "Heavy rain",
            66: "Light freezing rain", 67: "Heavy freezing rain",
            71: "Slight snow fall", 73: "Moderate snow fall", 75: "Heavy snow fall",
            77: "Snow grains",
            80: "Slight rain showers", 81: "Moderate rain showers", 82: "Heavy rain showers",
            85: "Slight snow showers", 86: "Heavy snow showers",
            95: "Thunderstorm", 96: "Thunderstorm with slight hail", 99: "Thunderstorm with heavy hail"
        }

        result["weather_description"] = weather_descriptions.get(
            current.get("weathercode"), "Unknown"
        )

        # Cache the result
        if use_cache:
            _weather_cache[cache_key] = (result, time.time())

        return result

    except requests.exceptions.Timeout:
        return {"error": "Weather service timeout. Please try again."}
    except requests.exceptions.ConnectionError:
        return {"error": "Unable to connect to weather service."}
    except requests.exceptions.HTTPError as e:
        return {"error": f"Weather service error: {e.response.status_code}"}
    except Exception as e:
        return {"error": f"Unexpected error: {str(e)}"}

def clear_weather_cache():
    """Clear the weather cache"""
    global _weather_cache
    _weather_cache.clear()
    return {"message": "Weather cache cleared."}