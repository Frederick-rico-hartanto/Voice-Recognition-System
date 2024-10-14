import requests
from utils.speak import speak
from utils.api_keys import OPEN_WEATHER_API_KEY


# Function to handle the weather command
def handle_weather(command):
    # Extract city name from the command
    if "weather" in command:
        city = command.replace("weather in", "").strip()

        if city:
            # API URL to fetch weather data from OpenWeatherMap
            url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={OPEN_WEATHER_API_KEY}"
            try:
                response = requests.get(url).json()
                if response["cod"] == 200:
                    # Extract weather description and temperature in Celsius
                    weather_description = response["weather"][0]["description"]
                    temp = response["main"]["temp"] - 273.15  # Convert from Kelvin to Celsius

                    # Speak the weather details
                    speak(
                        f"The weather in {city} is {weather_description} with a temperature of {temp:.2f} degrees Celsius.")
                else:
                    # Handle error if city is not found
                    speak(f"Sorry, I couldn't find the weather for {city}.")
            except Exception as e:
                speak(f"Sorry, there was an error fetching the weather data. {e}")
        else:
            speak("Please specify a city for the weather report.")
