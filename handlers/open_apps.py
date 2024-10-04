import subprocess
import os
from utils.speak import speak

# Cached paths for apps once found
cached_paths = {}

# Common directories to search for installed apps
common_directories = [
    "C:/Program Files/",
    "C:/Program Files (x86)/",
    os.path.expanduser("~") + "/AppData/Local/"
]

# Function to search for an app's executable file
def find_app_executable(app_name):
    if app_name in cached_paths:
        return cached_paths[app_name]

    # Go through common directories and search for the executable
    for directory in common_directories:
        for root, dirs, files in os.walk(directory):
            for file in files:
                if file.lower() == f"{app_name}.exe":
                    full_path = os.path.join(root, file)
                    cached_paths[app_name] = full_path
                    return full_path

    return None  # Return None if not found

# Function to open an app by searching for its executable
def open_app_by_search(app_name):
    executable_path = find_app_executable(app_name)

    if executable_path:
        try:
            speak(f"Opening {app_name}")
            subprocess.Popen([executable_path], shell=True)
        except Exception as e:
            speak(f"Failed to open {app_name}: {str(e)}")
    else:
        speak(f"Sorry, I couldn't find {app_name} on your system.")

# Function to handle Microsoft default apps
def open_microsoft_default_app(app_name):
    try:
        if app_name == "microsoft edge":
            speak("Opening Microsoft Edge")
            subprocess.Popen(["start", "msedge:"], shell=True)
        elif app_name == "settings":
            speak("Opening Settings")
            subprocess.Popen(["start", "ms-settings:"], shell=True)
        elif app_name == "control panel":
            speak("Opening Control Panel")
            subprocess.Popen(["control"], shell=True)
        elif app_name == "task manager":
            speak("Opening Task Manager")
            subprocess.Popen(["taskmgr"], shell=True)
        elif app_name == "file explorer":
            speak("Opening File Explorer")
            subprocess.Popen(["explorer"], shell=True)
        elif app_name == "command prompt":
            speak("Opening Command Prompt")
            subprocess.Popen(["cmd"], shell=True)
        elif app_name == "powershell":
            speak("Opening PowerShell")
            subprocess.Popen(["powershell"], shell=True)
        elif app_name == "calculator":
            speak("Opening Calculator")
            subprocess.Popen(["calc"], shell=True)
        elif app_name == "notepad":
            speak("Opening Notepad")
            subprocess.Popen(["notepad"], shell=True)
        elif app_name == "snipping tool":
            speak("Opening Snipping Tool")
            subprocess.Popen(["snippingtool"], shell=True)
        elif app_name == "microsoft store":
            speak("Opening Microsoft Store")
            subprocess.Popen(["start", "ms-windows-store:"], shell=True)
        elif app_name == "mail":
            speak("Opening Mail")
            subprocess.Popen(["start", "ms-mail:"], shell=True)
        elif app_name == "calendar":
            speak("Opening Calendar")
            subprocess.Popen(["start", "outlookcal:"], shell=True)
        elif app_name == "maps":
            speak("Opening Maps")
            subprocess.Popen(["start", "bingmaps:"], shell=True)
        elif app_name == "weather":
            speak("Opening Weather")
            subprocess.Popen(["start", "bingweather:"], shell=True)
        elif app_name == "xbox":
            speak("Opening Xbox")
            subprocess.Popen(["start", "xbox:"], shell=True)
        elif app_name == "word":
            speak("Opening Microsoft Word")
            subprocess.Popen(["C:/Program Files/Microsoft Office/root/Office16/WINWORD.EXE"], shell=True)
        elif app_name == "excel":
            speak("Opening Microsoft Excel")
            subprocess.Popen(["C:/Program Files/Microsoft Office/root/Office16/EXCEL.EXE"], shell=True)
        elif app_name == "powerpoint":
            speak("Opening Microsoft PowerPoint")
            subprocess.Popen(["C:/Program Files/Microsoft Office/root/Office16/POWERPNT.EXE"], shell=True)
        elif app_name == "outlook":
            speak("Opening Microsoft Outlook")
            subprocess.Popen(["C:/Program Files/Microsoft Office/root/Office16/OUTLOOK.EXE"], shell=True)
        else:
            return False  # App not recognized as a Microsoft default app
        return True  # Successfully handled as a Microsoft default app
    except Exception as e:
        speak(f"Failed to open {app_name}: {str(e)}")
        return True

# Main function to handle opening apps
def open_app(app_name):
    app_name = app_name.lower().replace(" ", "")  # Normalize app name (lowercase, remove spaces)

    # First, try to open as a Microsoft default app
    if open_microsoft_default_app(app_name):
        return

    # If not a Microsoft default app, try to search and open the app dynamically
    open_app_by_search(app_name)
