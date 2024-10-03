from utils.speak import speak

def handle_reminder_or_calendar(command):
    if "reminder" in command:
        reminder = command.replace("remind me to", "").strip()
        speak(f"Reminder set for: {reminder}")
        # Implement reminder logic using calendar API or task scheduler.
    elif "calendar" in command:
        event = command.replace("add to calendar", "").strip()
        speak(f"Adding event to your calendar: {event}")
        # Integrate with Google Calendar API or local calendar.
