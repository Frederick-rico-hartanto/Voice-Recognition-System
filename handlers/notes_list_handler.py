from utils.speak import speak

def handle_notes_or_lists(command):
    if "note" in command:
        note = command.replace("note", "").strip()
        speak(f"Adding note: {note}")
        # Save note in a local file or note-taking app
    elif "list" in command:
        list_item = command.replace("add", "").strip()
        speak(f"Adding {list_item} to your list.")
        # Add to a list (local or synced to app)
