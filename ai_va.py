import speech_recognition as sr
import os
import subprocess
import sys
import webbrowser
import pyttsx3
import smtplib
import requests
from email.mime.text import MIMEText
from googletrans import Translator
from datetime import datetime, timedelta  # For date and time management

from main import open_application

# Initialize text-to-speech engine
tts_engine = pyttsx3.init()

# Function to speak out text
def speak(text):
    tts_engine.say(text)
    tts_engine.runAndWait()

# Function to recognize speech, listen for wake word and full command in one step
def recognize_wake_and_command(prompt="Listening...", language="en-US"):
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print(prompt)
        speak(prompt)
        recognizer.adjust_for_ambient_noise(source, duration=1)
        try:
            # Allow more time to start speaking and finish a command
            audio = recognizer.listen(source, timeout=10, phrase_time_limit=15)
        except sr.WaitTimeoutError:
            print("Listening timed out while waiting for the phrase to start.")
            speak("I didn't hear anything. Please try again.")
            return None

    try:
        # Detect speech with multilingual support
        command = recognizer.recognize_google(audio, language=language)
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


# Function to check if the command starts with the wake word and extract the rest
def is_wake_word_detected(command):
    wake_words = ["hey bella", "ok bella", "okay bella"]
    for wake_word in wake_words:
        if command.startswith(wake_word):
            return True, command.replace(wake_word, "").strip()  # Remove the wake word from command
    return False, None


# Updated process_command function to better handle folder-specific requests
def process_command(command):
    wake_detected, actual_command = is_wake_word_detected(command)

    if not wake_detected:
        print("Wake word not detected. Waiting for valid command.")
        speak("Please start with Hey Bella or Okay Bella.")
        return

    # Translation detection comes first to avoid confusion with "what is" for search
    if is_translation_related(actual_command):
        phrase, lang = extract_translation(actual_command)
        translate_phrase(phrase, lang)
        return

    # Proceed with other command types
    if is_time_related(actual_command):
        handle_time_command(actual_command)

    elif is_date_related(actual_command):
        handle_date_command(actual_command)

    elif "call" in actual_command or "message" in actual_command:
        handle_call_message(actual_command)

    elif "email" in actual_command:
        handle_email(actual_command)

    elif "reminder" in actual_command or "calendar" in actual_command:
        handle_reminder_or_calendar(actual_command)

    elif "alarm" in actual_command or "timer" in actual_command:
        handle_alarm_timer(actual_command)

    elif "note" in actual_command or "list" in actual_command:
        handle_notes_or_lists(actual_command)

    elif "weather" in actual_command:
        handle_weather(actual_command)

    elif "convert" in actual_command:
        handle_unit_conversion(actual_command)

    elif "open" in actual_command and ("folder" in actual_command or "file" in actual_command):
        if "in desktop" in actual_command:
            folder_name = actual_command.replace("open the folder", "").replace("in desktop", "").strip()
            search_and_open_in_folder("desktop", folder_name)
        elif "in downloads" in actual_command:
            folder_name = actual_command.replace("open the folder", "").replace("in downloads", "").strip()
            search_and_open_in_folder("downloads", folder_name)
        elif "in documents" in actual_command:
            folder_name = actual_command.replace("open the folder", "").replace("in documents", "").strip()
            search_and_open_in_folder("documents", folder_name)
        elif "in pictures" in actual_command:
            folder_name = actual_command.replace("open the folder", "").replace("in pictures", "").strip()
            search_and_open_in_folder("pictures", folder_name)
        elif "in" in actual_command and "drive" in actual_command:
            parts = actual_command.split(" in ")
            item_name = parts[0].replace("open the folder", "").strip()
            drive_letter = parts[1].replace("drive", "").strip().upper()
            open_item_in_drive(item_name, drive_letter)
        else:
            print("Folder location not recognized or specified.")
            speak("Folder location not recognized or specified.")
        return None

    elif actual_command.startswith("open"):
        app_name = actual_command.replace("open", "").strip()
        print(f"Trying to open application: {app_name}")
        open_application(app_name)
        return None

    elif is_math_related(actual_command):
        equation = extract_equation(actual_command)
        solve_math_equation(equation)
        return None

    elif is_search_related(actual_command):
        search_query = actual_command.strip()  # Use the entire query as the search term
        search_online(search_query)
        return None

    else:
        print("Command not recognized.")
        speak("Command not recognized.")
        return None


# Function to detect if command is time-related
def is_time_related(command):
    keywords = ['time', 'clock', 'hour', 'minutes', 'now']
    return any(keyword in command for keyword in keywords)


# Function to detect if command is date-related
def is_date_related(command):
    keywords = ['date', 'day', 'today', 'tomorrow', 'yesterday', 'week', 'month', 'year']
    return any(keyword in command for keyword in keywords)


# Function to detect if a command is translation-related
def is_translation_related(command):
    return "in" in command and not any(char.isdigit() for char in command)  # No digits means it's likely translation


# Function to detect if a command is math-related
def is_math_related(command):
    math_symbols = ['+', '-', '*', '/', '=', '^']  # List of symbols to check for math operations
    return any(symbol in command for symbol in math_symbols) or any(char.isdigit() for char in command)


# Function to detect if command is search-related
def is_search_related(command):
    search_phrases = ["search for", "what is", "who is", "where is", "how to", "tell me about"]
    return any(phrase in command for phrase in search_phrases)


# Function to handle phone calls and messages
def handle_call_message(command):
    if "call" in command:
        person = command.replace("call", "").strip()
        speak(f"Calling {person}...")
        # Implement phone call logic using Twilio or similar API if needed.
    elif "message" in command:
        person = command.replace("message", "").strip().split("to")[1]
        speak(f"Messaging {person}...")
        # Implement message sending logic with Twilio or similar API.


# Function to handle email
def handle_email(command):
    subject = command.split("email")[1].strip()
    speak("Please speak the message.")
    message_body = recognize_wake_and_command(prompt="Listening for your message...")
    if message_body:
        send_email(subject, message_body)


# Function to send email via SMTP
def send_email(subject, body):
    sender = "your-email@example.com"
    recipient = "recipient@example.com"
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = recipient
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender, "your-password")
        server.sendmail(sender, recipient, msg.as_string())
        server.quit()
        speak("Email sent successfully.")
    except Exception as e:
        speak("Error sending email.")


# Function to handle calendar and reminders
def handle_reminder_or_calendar(command):
    if "reminder" in command:
        reminder = command.replace("remind me to", "").strip()
        speak(f"Reminder set for: {reminder}")
        # Implement reminder logic using calendar API or task scheduler.
    elif "calendar" in command:
        event = command.replace("add to calendar", "").strip()
        speak(f"Adding event to your calendar: {event}")
        # Integrate with Google Calendar API or local calendar.


# Function to handle alarms, timers, and clock
def handle_alarm_timer(command):
    if "alarm" in command:
        time = command.split("alarm for")[1].strip()
        speak(f"Setting alarm for {time}.")
        # Implement alarm logic
    elif "timer" in command:
        duration = command.split("timer for")[1].strip()
        speak(f"Setting a timer for {duration}.")
        # Implement timer logic


# Function to handle notes and lists
def handle_notes_or_lists(command):
    if "note" in command:
        note = command.replace("note", "").strip()
        speak(f"Adding note: {note}")
        # Save note in a local file or note-taking app
    elif "list" in command:
        list_item = command.replace("add", "").strip()
        speak(f"Adding {list_item} to your list.")
        # Add to a list (local or synced to app)


# Function to handle weather updates
def handle_weather(command):
    city = command.replace("weather in", "").strip()
    api_key = "your_openweather_api_key"
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"
    response = requests.get(url).json()
    if response["cod"] == 200:
        weather_description = response["weather"][0]["description"]
        temp = response["main"]["temp"] - 273.15  # Convert Kelvin to Celsius
        speak(f"The weather in {city} is {weather_description} with a temperature of {temp:.2f}°C.")
    else:
        speak("Sorry, I couldn't get the weather information.")


# Function to handle unit conversions
def handle_unit_conversion(command):
    # Example: "convert 10 dollars to euros"
    speak("Unit conversion is not yet implemented.")
    # Integrate currency or unit conversion APIs.


# Function to handle time-related commands
def handle_time_command(command):
    current_time = datetime.now().strftime("%I:%M %p")  # 12-hour format with AM/PM
    print(f"The current time is {current_time}")
    speak(f"The current time is {current_time}")


# Function to handle date-related commands
def handle_date_command(command):
    if 'tomorrow' in command:
        date = (datetime.now() + timedelta(days=1)).strftime("%A, %B %d, %Y")
        print(f"Tomorrow's date is {date}")
        speak(f"Tomorrow's date is {date}")
    elif 'yesterday' in command:
        date = (datetime.now() - timedelta(days=1)).strftime("%A, %B %d, %Y")
        print(f"Yesterday's date was {date}")
        speak(f"Yesterday's date was {date}")
    else:
        date = datetime.now().strftime("%A, %B %d, %Y")  # Get today's date
        print(f"Today's date is {date}")
        speak(f"Today's date is {date}")


# Function to get common folder paths dynamically (Desktop, Downloads, etc.)
def get_common_folder_path(folder_type):
    home_dir = os.path.expanduser("~")
    if folder_type == "desktop":
        return os.path.join(home_dir, "Desktop")
    elif folder_type == "downloads":
        return os.path.join(home_dir, "Downloads")
    elif folder_type == "documents":
        return os.path.join(home_dir, "Documents")
    elif folder_type == "pictures":
        return os.path.join(home_dir, "Pictures")
    elif folder_type == "music":
        return os.path.join(home_dir, "Music")
    elif folder_type == "videos":
        return os.path.join(home_dir, "Videos")
    else:
        return None


# Function to open a file or folder
def open_file_or_folder(path):
    if os.path.exists(path):
        print(f"Opening: {path}")
        speak(f"Opening {os.path.basename(path)}.")
        if sys.platform == "win32":
            subprocess.run(["explorer", path])
        elif sys.platform == "darwin":
            subprocess.run(["open", path])
        else:  # Linux or other OS
            subprocess.run(["xdg-open", path])
    else:
        print(f"'{path}' not found.")
        speak(f"Sorry, {os.path.basename(path)} was not found.")


# Function to search and open a file or folder in a specific location (folder_type could be desktop, downloads, etc.)
def search_and_open_in_folder(folder_type, item_name):
    folder_path = get_common_folder_path(folder_type)
    if folder_path is None:
        print(f"Unknown folder type: {folder_type}")
        speak(f"Sorry, I don't know how to search in {folder_type}.")
        return

    item_name = item_name.lower()  # Case-insensitive search
    print(f"Searching for '{item_name}' in {folder_type} ({folder_path})...")
    speak(f"Searching for {item_name} in {folder_type}...")

    # Walk through the folder to search for both files and folders
    for root, dirs, files in os.walk(folder_path):
        for dir_name in dirs:
            if item_name == dir_name.lower():  # Case-insensitive match for folders
                open_file_or_folder(os.path.join(root, dir_name))
                return
        for file_name in files:
            if item_name == file_name.lower():  # Case-insensitive match for files
                open_file_or_folder(os.path.join(root, file_name))
                return

    print(f"'{item_name}' not found in {folder_type}.")
    speak(f"Sorry, {item_name} was not found in {folder_type}.")


# Function to open a folder or file in a specific drive
def open_item_in_drive(item_name, drive_letter):
    drive_path = f"{drive_letter}:/"
    item_name = item_name.lower()  # Case-insensitive search
    print(f"Searching for '{item_name}' in {drive_letter} drive...")
    speak(f"Searching for {item_name} in {drive_letter} drive...")

    # Walk through the drive to search for both files and folders
    for root, dirs, files in os.walk(drive_path):
        for dir_name in dirs:
            if item_name == dir_name.lower():  # Case-insensitive match for folders
                open_file_or_folder(os.path.join(root, dir_name))
                return
        for file_name in files:
            if item_name == file_name.lower():  # Case-insensitive match for files
                open_file_or_folder(os.path.join(root, file_name))
                return

    print(f"'{item_name}' not found in {drive_letter} drive.")
    speak(f"Sorry, {item_name} was not found in {drive_letter} drive.")


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
        phrase = parts[0].replace("translate", "").replace("what is", "").strip()
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


# Main loop to listen for wake word and execute commands immediately after detection
if __name__ == "__main__":
    while True:
        command = recognize_wake_and_command(prompt="Listening for your command with wake word...")
        if command:
            process_command(command)
            if "quit" in command or "exit" in command:
                print("Exiting voice assistant.")
                speak("Exiting voice assistant.")
                break
