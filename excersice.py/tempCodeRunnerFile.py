import requests
import json
import os
from datetime import datetime

API_KEY = "YOUR_API_KEY_HERE"  # 👈 Paste your OpenWeatherMap API key here
BASE_URL = "http://api.openweathermap.org/data/2.5/weather"
HISTORY_FILE = "weather_history.json"


def get_weather(city):
    params = {
        "q": city,
        "appid": API_KEY,
        "units": "metric"  # Use "imperial" for Fahrenheit
    }
    try:
        response = requests.get(BASE_URL, params=params, timeout=5)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError:
        print(f"❌ City '{city}' not found. Check spelling and try again.")
    except requests.exceptions.ConnectionError:
        print("❌ No internet connection. Please check your network.")
    except requests.exceptions.Timeout:
        print("❌ Request timed out. Try again.")
    except Exception as e:
        print(f"❌ Something went wrong: {e}")
    return None


def display_weather(data):
    city = data["name"]
    country = data["sys"]["country"]
    temp = data["main"]["temp"]
    feels_like = data["main"]["feels_like"]
    humidity = data["main"]["humidity"]
    description = data["weather"][0]["description"].title()
    wind_speed = data["wind"]["speed"]

    print("\n" + "=" * 40)
    print(f"🌍 Weather in {city}, {country}")
    print("=" * 40)
    print(f"🌡️  Temperature : {temp}°C (feels like {feels_like}°C)")
    print(f"☁️  Condition   : {description}")
    print(f"💧 Humidity    : {humidity}%")
    print(f"💨 Wind Speed  : {wind_speed} m/s")
    print("=" * 40 + "\n")


def save_to_history(city, data):
    history = load_history()
    entry = {
        "city": city,
        "temp": data["main"]["temp"],
        "description": data["weather"][0]["description"],
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    history.append(entry)

    with open(HISTORY_FILE, "w") as f:
        json.dump(history, f, indent=2)


def load_history():
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return []
    return []


def show_history():
    history = load_history()
    if not history:
        print("📭 No search history yet.")
        return

    print("\n📜 Search History:")
    print("-" * 40)
    for entry in history[-5:]:  # show last 5
        print(f"{entry['timestamp']} | {entry['city']} | {entry['temp']}°C | {entry['description']}")
    print("-" * 40 + "\n")


def main():
    print("🌤️  Welcome to the Weather CLI App!")
    print("Type 'history' to see past searches, or 'quit' to exit.\n")

    while True:
        city = input("Enter a city name: ").strip()

        if city.lower() == "quit":
            print("👋 Goodbye!")
            break
        elif city.lower() == "history":
            show_history()
            continue
        elif not city:
            print("⚠️  Please enter a city name.\n")
            continue

        data = get_weather(city)
        if data:
            display_weather(data)
            save_to_history(city, data)


if __name__ == "__main__":
    main()