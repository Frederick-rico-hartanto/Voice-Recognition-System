import speech_recognition as sr
import os
import subprocess
import sys
import webbrowser
import pyttsx3
from googletrans import Translator

from main import open_application

# Initialize text-to-speech engine
tts_engine = pyttsx3.init()

# Function to speak out text
def speak(text):
    tts_engine.say(text)
    tts_engine.runAndWait()

# Function to recognize speech from the microphone
def recognize_speech(prompt="Listening..."):
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print(prompt)
        speak(prompt)
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    try:
        # Convert speech to text
        command = recognizer.recognize_google(audio)
        print(f"Recognized command: {command}")
        return command.lower()
    except sr.UnknownValueError:
        print("Sorry, I could not understand the audio.")
        speak("Sorry, I could not understand the audio.")
        return None
    except sr.RequestError:
        print("Sorry, there was a problem with the request.")
        speak("Sorry, there was a problem with the request.")
        return None


# Function to check if the wake word is used and extract the actual command
def process_command(command):
    if command.startswith("open"):
        app_name = command.replace("open", "").strip()
        return app_name
    elif is_math_related(command):
        equation = extract_equation(command)
        solve_math_equation(equation)  # Solve and return, no need for further processing
        return None  # Prevent further processing of the result
    elif "search" in command or "what is" in command:
        search_query = command.replace("search for", "").replace("what is", "").strip()
        search_online(search_query)
        return None
    elif command.startswith("translate"):
        phrase, lang = extract_translation(command)
        return translate_phrase(phrase, lang)
    else:
        print("Command not recognized.")
        speak("Command not recognized.")
        return None


# Function to determine if a command is math-related
def is_math_related(command):
    math_related_phrases = ['solve', 'calculate', 'what is', 'find', 'evaluate', 'compute']
    return any(phrase in command for phrase in math_related_phrases)


# Function to extract mathematical equation from the command
def extract_equation(command):
    math_related_phrases = ['solve', 'calculate', 'what is', 'find', 'evaluate', 'compute']
    for phrase in math_related_phrases:
        if phrase in command:
            return command.replace(phrase, "").strip()
    return command


# Function to solve mathematical equations using eval (for simple cases)
def solve_math_equation(equation):
    try:
        result = eval(equation)
        print(f"The result of {equation} is {result}")
        speak(f"The result of {equation} is {result}")
        return result
    except Exception as e:
        print(f"Error solving equation: {e}")
        speak("Error solving the equation")
        return None


# Function to perform a web search
def search_online(query):
    try:
        print(f"Searching online for: {query}")
        speak(f"Searching online for {query}")
        webbrowser.open(f"https://www.google.com/search?q={query}")
    except Exception as e:
        print(f"Error performing search: {e}")
        speak("Error performing the search")


# Function to extract the phrase and language for translation
def extract_translation(command):
    parts = command.split("in")
    if len(parts) == 2:
        phrase = parts[0].replace("translate", "").strip()
        lang = parts[1].strip()
        return phrase, lang
    return command, 'en'


# Function to translate a given phrase using googletrans
def translate_phrase(phrase, lang='en'):
    translator = Translator()
    try:
        translated = translator.translate(phrase, dest=lang)
        print(f"Translation: {translated.text}")
        speak(f"Translation: {translated.text}")
        return translated.text
    except Exception as e:
        print(f"Error translating phrase: {e}")
        speak("Error translating the phrase")
        return None


# Handle Microsoft-specific applications using system commands or known paths
def handle_microsoft_apps(app_name):
    app_name_lower = app_name.lower()

    if app_name_lower in ["microsoft edge", "edge"]:
        print("Opening Microsoft Edge...")
        speak("Opening Microsoft Edge...")
        subprocess.run(["start", "msedge"], shell=True)
        return True
    elif app_name_lower in ["microsoft store", "store"]:
        print("Opening Microsoft Store...")
        speak("Opening Microsoft Store...")
        subprocess.run(["start", "ms-windows-store:"], shell=True)
        return True
    elif app_name_lower in ["microsoft excel", "excel"]:
        print("Opening Microsoft Excel...")
        speak("Opening Microsoft Excel...")
        excel_path = "C:/Program Files/Microsoft Office/root/Office16/EXCEL.EXE"
        if os.path.exists(excel_path):
            os.startfile(excel_path)
        else:
            print("Excel executable not found.")
            speak("Excel executable not found.")
        return True
    elif app_name_lower in ["microsoft word", "word"]:
        print("Opening Microsoft Word...")
        speak("Opening Microsoft Word...")
        word_path = "C:/Program Files/Microsoft Office/root/Office16/WINWORD.EXE"
        if os.path.exists(word_path):
            os.startfile(word_path)
        else:
            print("Word executable not found.")
            speak("Word executable not found.")
        return True
    elif app_name_lower in ["microsoft powerpoint", "powerpoint"]:
        print("Opening Microsoft PowerPoint...")
        speak("Opening Microsoft PowerPoint...")
        ppt_path = "C:/Program Files/Microsoft Office/root/Office16/POWERPNT.EXE"
        if os.path.exists(ppt_path):
            os.startfile(ppt_path)
        else:
            print("PowerPoint executable not found.")
            speak("PowerPoint executable not found.")
        return True

    return False


# Main function to listen for the wake word "Hey Bella", "Ok Bella", or "Okay Bella"
# Main function to listen for the wake word "Hey Bella", "Ok Bella", or "Okay Bella"
def listen_for_wake_word():
    print("Listening for wake words 'Hey Bella', 'Ok Bella', or 'Okay Bella'...")
    speak("Listening for wake words 'Hey Bella', 'Ok Bella', or 'Okay Bella'...")

    while True:
        command = recognize_speech(prompt="Listening for 'Hey Bella', 'Ok Bella', or 'Okay Bella'...")

        if command and ("hey bella" in command or "ok bella" in command or "okay bella" in command):
            print("Wake word detected!")
            speak("Wake word detected!")
            return True


# Main loop
if __name__ == "__main__":
    while True:
        if listen_for_wake_word():
            command = recognize_speech(prompt="You can now give a command...")
            if command:
                app_name = process_command(command)
                if app_name:
                    open_application(app_name)
                elif "quit" in command or "exit" in command:
                    print("Exiting voice assistant.")
                    speak("Exiting voice assistant.")
                    break
