import requests
from utils.speak import speak
from utils.api_keys import OPEN_WEATHER_API_KEY

def handle_weather(command):
    city = command.replace("weather in", "").strip()
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={OPEN_WEATHER_API_KEY}"
    response = requests.get(url).json()
    if response["cod"] == 200:
        weather_description = response["weather"][0]["description"]
        temp = response["main"]["temp"] - 273.15  # Convert Kelvin to Celsius
        speak(f"The weather in {city} is {weather_description} with a temperature of {temp:.2f}°C.")
    else:
        speak("Sorry, I couldn't get the weather information.")
