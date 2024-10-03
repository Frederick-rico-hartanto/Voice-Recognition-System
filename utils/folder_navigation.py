import os
import subprocess
import sys
from utils.speak import speak

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
