
import json
from datetime import datetime
import urllib.parse
import urllib.request
import time


def fetch_data(url):
    """Fetch JSON data with retries for temporary connection failures."""

    for attempt in range(1, 4):
        try:
            with urllib.request.urlopen(url, timeout=10) as response:
                return json.loads(response.read().decode("utf-8"))

        except urllib.error.HTTPError as error:
            print(f"HTTP error: {error.code} - {error.reason}")
            return None

        except urllib.error.URLError as error:
            print(f"Connection attempt {attempt} failed: {error.reason}")

            if attempt < 3:
                print("Retrying in 2 seconds...")
                time.sleep(2)

    print("Unable to retrieve data after 3 attempts.")
    return None


def get_coordinates(city):
    """Find a city's latitude and longitude using Open-Meteo."""

    url = "https://geocoding-api.open-meteo.com/v1/search?" + urllib.parse.urlencode({
        "name": city,
        "count": 1,
        "language": "en",
        "format": "json"
    })

    data = fetch_data(url)

    if data is None:
        return None

    results = data.get("results", [])

    if not results:
        print(f"Sorry, I couldn't find {city}.")
        return None

    location = results[0]

    return {
        "name": location["name"],
        "country": location.get("country", "Unknown"),
        "latitude": location["latitude"],
        "longitude": location["longitude"]
    }


def get_weather(latitude, longitude):
    """Get current weather information using coordinates."""

    url = "https://api.open-meteo.com/v1/forecast?" + urllib.parse.urlencode({
        "latitude": latitude,
        "longitude": longitude,
        "current": "temperature_2m,relative_humidity_2m,wind_speed_10m,weather_code",
        "timezone": "auto"
    })

    data = fetch_data(url)

    if data is None:
        return None

    return data["current"]


def get_forecast(latitude, longitude):
    """Get a 7-day weather forecast."""

    url = "https://api.open-meteo.com/v1/forecast?" + urllib.parse.urlencode({
        "latitude": latitude,
        "longitude": longitude,
        "daily": "weather_code,temperature_2m_max,temperature_2m_min",
        "forecast_days": 7,
        "timezone": "auto"
    })

    data = fetch_data(url)

    if data is None:
        return None

    return data["daily"]


def get_weather_description(code):
    """Convert WMO weather codes into readable descriptions."""

    weather_conditions = {
        0: "Clear sky ☀️",
        1: "Mainly clear 🌤️",
        2: "Partly cloudy ⛅",
        3: "Overcast ☁️",
        45: "Fog 🌫️",
        48: "Depositing rime fog 🌫️",
        51: "Light drizzle 🌦️",
        53: "Moderate drizzle 🌦️",
        55: "Dense drizzle 🌧️",
        61: "Slight rain 🌧️",
        63: "Moderate rain 🌧️",
        65: "Heavy rain 🌧️",
        71: "Slight snowfall 🌨️",
        73: "Moderate snowfall 🌨️",
        75: "Heavy snowfall ❄️",
        80: "Slight rain showers 🌦️",
        81: "Moderate rain showers 🌧️",
        82: "Violent rain showers ⛈️",
        95: "Thunderstorm ⛈️",
        96: "Thunderstorm with slight hail ⛈️",
        99: "Thunderstorm with heavy hail ⛈️"
    }

    return weather_conditions.get(code, "Unknown weather condition")


# Main application
if __name__ == "__main__":

    city = input("Enter a city name: ").strip()

    if not city:
        print("Please enter a city name.")

    else:
        location = get_coordinates(city)

        if location:
            print("\n" + "=" * 40)
            print("           WEATHER REPORT")
            print("=" * 40)

            print(f"Location: {location['name']}, {location['country']}")

            weather = get_weather(
                location["latitude"],
                location["longitude"]
            )

            if weather:
                observation_time = datetime.fromisoformat(weather["time"])
                formatted_time = observation_time.strftime("%H:%M")

                description = get_weather_description(weather["weather_code"])

                print(f"Local time: {formatted_time}")

                print("\nCURRENT WEATHER")
                print("-" * 40)
                print(f"Condition: {description}")
                print(f"Temperature: {weather['temperature_2m']} °C")
                print(f"Humidity: {weather['relative_humidity_2m']} %")
                print(f"Wind speed: {weather['wind_speed_10m']} km/h")

            forecast = get_forecast(
                location["latitude"],
                location["longitude"]
            )

            if forecast:
                print("\n7-DAY FORECAST")
                print("-" * 40)

                for date, max_temp, min_temp, code in zip(
                    forecast["time"],
                    forecast["temperature_2m_max"],
                    forecast["temperature_2m_min"],
                    forecast["weather_code"]
                ):
                    formatted_date = datetime.strptime(
                        date, "%Y-%m-%d"
                    ).strftime("%a %d %b")

                    description = get_weather_description(code)

                    print(f"{formatted_date} | {description}")
                    print(f"             Max: {max_temp} °C")
                    print(f"             Min: {min_temp} °C")
                    print()

            print("=" * 40)
