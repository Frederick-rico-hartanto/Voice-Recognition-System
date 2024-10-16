import sys
import os

# Ensure the parent directory is in the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import speech_recognition as sr
from utils.speak import speak

def recognize_wake_and_command(prompt="Listening...", language="en-US"):
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        speak(prompt)
        recognizer.adjust_for_ambient_noise(source, duration=1)
        try:
            audio = recognizer.listen(source, timeout=10, phrase_time_limit=15)
        except sr.WaitTimeoutError:
            speak("I didn't hear anything. Please try again.")
            return None

    try:
        command = recognizer.recognize_google(audio, language=language)
        return command.lower()
    except sr.UnknownValueError:
        speak("Sorry, I could not understand the audio.")
        return None
    except sr.RequestError:
        speak("Sorry, there was a problem with the request.")
        return None

# Function to detect if a command is time-related
def is_time_related(command):
    keywords = ['time', 'clock', 'hour', 'minutes', 'now']
    return any(keyword in command for keyword in keywords)

# Function to detect if a command is date-related
def is_date_related(command):
    keywords = ['date', 'day', 'today', 'tomorrow', 'yesterday', 'week', 'month', 'year']
    return any(keyword in command for keyword in keywords)

# Function to detect if command is search-related
def is_search_related(command):
    search_phrases = ["search for", "what is", "who is", "where is", "how to", "tell me about"]
    return any(phrase in command for phrase in search_phrases)

# Function to detect if a command is translation-related
def is_translation_related(command):
    # Detect if the command involves translation, including "what is ... in" pattern
    return "translate" in command or ("what is" in command and "in" in command)

# Additional function to detect if a command is math-related
def is_math_related(command):
    return any(char.isdigit() for char in command) and any(symbol in command for symbol in ['+', '-', '*', '/', '='])