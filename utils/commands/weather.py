import os
import requests

CITY = "Bangalore"


def get_weather():
    api_key = os.getenv("OPENWEATHER_API_KEY")

    if not api_key:
        return "Weather is not configured yet. Please add your OpenWeather API key."

    try:
        response = requests.get(
            "https://api.openweathermap.org/data/2.5/weather",
            params={"q": CITY, "appid": api_key, "units": "metric"},
            timeout=8,
        )
        data = response.json()

        if data.get("cod") != 200:
            return "I couldn't get the weather."

        temperature = data["main"]["temp"]
        condition = data["weather"][0]["description"]

        return f"The temperature in {CITY} is {temperature} degrees Celsius with {condition}."

    except Exception:
        return "Unable to fetch the weather."
