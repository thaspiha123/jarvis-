import requests

API_KEY = "c218b440e77f0bb1d02ac041f1746f92"
CITY = "Bangalore"


def get_weather():
    url = (
        f"https://api.openweathermap.org/data/2.5/weather"
        f"?q={CITY}&appid={API_KEY}&units=metric"
    )

    try:
        response = requests.get(url)
        data = response.json()

        if data.get("cod") != 200:
            return "I couldn't get the weather."

        temperature = data["main"]["temp"]
        condition = data["weather"][0]["description"]

        return f"The temperature in {CITY} is {temperature} degrees Celsius with {condition}."

    except Exception:
        return "Unable to fetch the weather."