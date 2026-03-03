# tools/weather_tool.py

import requests


def get_weather(lat: float, lon: float) -> dict:
    """
    Lấy thông tin thời tiết hiện tại theo GPS.
    Sử dụng Open-Meteo API (free, không cần API key)
    """

    url = (
        f"https://api.open-meteo.com/v1/forecast"
        f"?latitude={lat}&longitude={lon}"
        f"&current_weather=true"
    )

    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        current = data.get("current_weather", {})

        return {
            "temperature": current.get("temperature"),
            "windspeed": current.get("windspeed"),
            "winddirection": current.get("winddirection"),
            "weathercode": current.get("weathercode"),
        }

    except Exception as e:
        return {"error": str(e)}