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
            subprocess.run(["explorer", path], check=True)
        elif sys.platform == "darwin":
            subprocess.run(["open", path], check=True)
        else:  # Linux or other OS
            subprocess.run(["xdg-open", path], check=True)
    else:
        print(f"'{path}' not found.")
        speak(f"Sorry, {os.path.basename(path)} was not found.")


# Function to list all contents of a folder
def list_folder_contents(folder_type):
    folder_path = get_common_folder_path(folder_type)
    if folder_path is None:
        print(f"Unknown folder type: {folder_type}")
        speak(f"Sorry, I don't know how to search in {folder_type}.")
        return

    print(f"Listing all contents in {folder_type} ({folder_path}):")
    if os.path.exists(folder_path):
        for root, dirs, files in os.walk(folder_path):
            print(f"\nIn Directory: {root}")
            print(f"Directories: {dirs}")
            print(f"Files: {files}")
    else:
        print(f"Error: {folder_path} does not exist!")


# Function to search and open a file or folder in a specific location (folder_type could be desktop, downloads, etc.)
def search_and_open_in_folder(folder_type, item_name):
    folder_path = get_common_folder_path(folder_type)

    if folder_path is None:
        print(f"Unknown folder type: {folder_type}")
        speak(f"Sorry, I don't know how to search in {folder_type}.")
        return

    # Normalize the item name for search
    item_name = item_name.lower().strip()
    print(f"Searching for '{item_name}' in {folder_type} at ({folder_path})...")
    speak(f"Searching for {item_name} in {folder_type}...")

    # Walk through the folder to search for both files and folders
    found = False
    for root, dirs, files in os.walk(folder_path):
        print(f"Checking in directory: {root}")  # Debugging: Print current directory being checked

        # Check if folder matches
        for dir_name in dirs:
            normalized_dir_name = dir_name.lower().strip()
            print(f"Found directory: {dir_name}")  # Debugging: list directories being checked
            if item_name in normalized_dir_name:  # More flexible match
                print(f"Folder match found: {os.path.join(root, dir_name)}")
                open_file_or_folder(os.path.join(root, dir_name))
                found = True
                return

        # Check if file matches
        for file_name in files:
            normalized_file_name = file_name.lower().strip()
            print(f"Found file: {file_name}")  # Debugging: list files being checked
            if item_name in normalized_file_name:  # More flexible match
                print(f"File match found: {os.path.join(root, file_name)}")
                open_file_or_folder(os.path.join(root, file_name))
                found = True
                return

    if not found:
        print(f"'{item_name}' not found in {folder_type}.")
        speak(f"Sorry, {item_name} was not found in {folder_type}.")


# Function to check if the common folder paths are correct
def debug_common_folders():
    print("Desktop Path: ", get_common_folder_path("desktop"))
    print("Downloads Path: ", get_common_folder_path("downloads"))
    print("Documents Path: ", get_common_folder_path("documents"))
    print("Pictures Path: ", get_common_folder_path("pictures"))
    print("Music Path: ", get_common_folder_path("music"))
    print("Videos Path: ", get_common_folder_path("videos"))


# Test if folder paths are correctly retrieved
debug_common_folders()

# List contents of the desktop to verify it
list_folder_contents("desktop")

# Search and open a folder or file on Desktop, for example:
# Replace "folder_name_or_file_name" with the folder or file name you want to search for
search_and_open_in_folder("desktop", "folder_navigation.py")
