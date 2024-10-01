import speech_recognition as sr
import os
import subprocess
import sys
import webbrowser
from googletrans import Translator


# Function to recognize speech from the microphone
def recognize_speech(prompt="Listening..."):
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print(prompt)
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    try:
        # Convert speech to text
        command = recognizer.recognize_google(audio)
        print(f"Recognized command: {command}")
        return command.lower()
    except sr.UnknownValueError:
        print("Sorry, I could not understand the audio.")
        return None
    except sr.RequestError:
        print("Sorry, there was a problem with the request.")
        return None


# Function to check if the wake word is used and extract the actual command
def process_command(command):
    if command.startswith("open"):
        app_name = command.replace("open", "").strip()
        return app_name
    elif is_math_related(command):
        equation = extract_equation(command)
        return solve_math_equation(equation)
    elif "search" in command or "what is" in command:
        search_query = command.replace("search for", "").replace("what is", "").strip()
        search_online(search_query)
        return None
    elif command.startswith("translate"):
        phrase, lang = extract_translation(command)
        return translate_phrase(phrase, lang)
    else:
        print("Command not recognized after wake word.")
        return None


# Function to determine if a command is math-related
def is_math_related(command):
    math_related_phrases = ['solve', 'calculate', 'what is', 'find', 'evaluate', 'compute']
    return any(phrase in command for phrase in math_related_phrases)


# Function to extract mathematical equation from the command
def extract_equation(command):
    # Remove the math-related phrase to leave the equation
    math_related_phrases = ['solve', 'calculate', 'what is', 'find', 'evaluate', 'compute']
    for phrase in math_related_phrases:
        if phrase in command:
            return command.replace(phrase, "").strip()
    return command


# Function to solve mathematical equations using eval (for simple cases)
def solve_math_equation(equation):
    try:
        # Safely evaluate the mathematical expression
        result = eval(equation)
        print(f"The result of {equation} is {result}")
        return f"The result of {equation} is {result}"
    except Exception as e:
        print(f"Error solving equation: {e}")
        return "Error solving the equation"


# Function to perform a web search
def search_online(query):
    try:
        print(f"Searching online for: {query}")
        webbrowser.open(f"https://www.google.com/search?q={query}")
    except Exception as e:
        print(f"Error performing search: {e}")


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
        return f"Translation: {translated.text}"
    except Exception as e:
        print(f"Error translating phrase: {e}")
        return "Error translating the phrase"


# Handle Microsoft-specific applications using system commands or known paths
def handle_microsoft_apps(app_name):
    app_name_lower = app_name.lower()

    if app_name_lower in ["microsoft edge", "edge"]:
        print("Opening Microsoft Edge...")
        subprocess.run(["start", "msedge"], shell=True)
        return True
    elif app_name_lower in ["microsoft store", "store"]:
        print("Opening Microsoft Store...")
        subprocess.run(["start", "ms-windows-store:"], shell=True)
        return True
    elif app_name_lower in ["microsoft excel", "excel"]:
        print("Opening Microsoft Excel...")
        excel_path = "C:/Program Files/Microsoft Office/root/Office16/EXCEL.EXE"
        if os.path.exists(excel_path):
            os.startfile(excel_path)
        else:
            print("Excel executable not found.")
        return True
    elif app_name_lower in ["microsoft word", "word"]:
        print("Opening Microsoft Word...")
        word_path = "C:/Program Files/Microsoft Office/root/Office16/WINWORD.EXE"
        if os.path.exists(word_path):
            os.startfile(word_path)
        else:
            print("Word executable not found.")
        return True
    elif app_name_lower in ["microsoft powerpoint", "powerpoint"]:
        print("Opening Microsoft PowerPoint...")
        ppt_path = "C:/Program Files/Microsoft Office/root/Office16/POWERPNT.EXE"
        if os.path.exists(ppt_path):
            os.startfile(ppt_path)
        else:
            print("PowerPoint executable not found.")
        return True

    return False


# Fallback function to search for apps in Program Files
def find_app_in_program_files(app_name):
    common_paths = [
        "C:/Program Files",
        "C:/Program Files (x86)"
    ]

    exclude_terms = ["service", "helper", "updater", "util", "xbox", "assistant", "daemon"]

    preferred_executable = f"{app_name}.exe"

    for path in common_paths:
        for root, dirs, files in os.walk(path):
            for file in files:
                if file.lower() == preferred_executable.lower():
                    return os.path.join(root, file)

            for file in files:
                if app_name.lower() in file.lower() and file.endswith(".exe"):
                    if not any(exclude in file.lower() for exclude in exclude_terms):
                        return os.path.join(root, file)

    return None


# Function to open applications based on the platform
def open_application(app_name):
    try:
        if sys.platform == "win32":  # For Windows
            if handle_microsoft_apps(app_name):
                return

            app_path = find_app_in_program_files(app_name)
            if app_path:
                print(f"Found {app_name} at {app_path}, opening...")
                os.startfile(app_path)
            else:
                print(f"Application {app_name} is not recognized or not found.")
        elif sys.platform == "darwin":  # For macOS
            subprocess.call(["open", f"/Applications/{app_name}.app"])
        elif sys.platform == "linux":  # For Linux
            subprocess.call([app_name])
        else:
            print("Unsupported operating system.")
    except Exception as e:
        print(f"Failed to open {app_name}: {e}")


# Function to open system settings based on the platform
def open_settings():
    try:
        if sys.platform == "win32":  # For Windows
            print("Opening Windows Settings...")
            subprocess.run(["start", "ms-settings:"], shell=True)
        elif sys.platform == "darwin":  # For macOS
            print("Opening macOS System Preferences...")
            subprocess.run(["open", "/System/Library/PreferencePanes"], shell=True)
        elif sys.platform.startswith("linux"):  # For Linux
            print("Opening Linux System Settings...")
            subprocess.run(["gnome-control-center"])  # Works on GNOME-based systems, adjust for others
        else:
            print("Unsupported operating system for settings.")
    except Exception as e:
        print("Failed to open settings: {e}")


# Main function that listens for the wake word "Hey Lumi"
def listen_for_wake_word():
    print("Listening for wake word 'Hey Lumi'...")

    while True:
        command = recognize_speech(prompt="Listening for 'Hey Lumi'...")

        if command and "hey lumi" in command:
            print("Wake word 'Hey Lumi' detected!")
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
                    break
