from utils.speak import speak
from utils.command_recognition import recognize_wake_and_command
from handlers.email_handler import handle_email
from handlers.call_message_handler import handle_call_message
from handlers.calendar_reminder_handler import handle_reminder_or_calendar
from handlers.alarm_timer_handler import handle_alarm_timer
from handlers.notes_list_handler import handle_notes_or_lists
from handlers.weather_handler import handle_weather
from handlers.unit_conversion_handler import handle_unit_conversion
from utils.time_date_handler import handle_time_command, handle_date_command
from handlers.search_handler import search_online
from handlers.translation_handler import translate_phrase

def process_command(command):
    if "call" in command or "message" in command:
        handle_call_message(command)
    elif "email" in command:
        handle_email(command)
    elif "reminder" in command or "calendar" in command:
        handle_reminder_or_calendar(command)
    elif "alarm" in command or "timer" in command:
        handle_alarm_timer(command)
    elif "note" in command or "list" in command:
        handle_notes_or_lists(command)
    elif "weather" in command:
        handle_weather(command)
    elif "convert" in command:
        handle_unit_conversion(command)
    elif is_time_related(command):
        handle_time_command(command)
    elif is_date_related(command):
        handle_date_command(command)
    elif is_search_related(command):
        search_online(command)
    elif is_translation_related(command):
        phrase, lang = extract_translation(command)
        translate_phrase(phrase, lang)
    else:
        speak("Command not recognized.")

# Main loop
if __name__ == "__main__":
    while True:
        command = recognize_wake_and_command(prompt="Listening for your command with wake word...")
        if command:
            process_command(command)
            if "quit" in command or "exit" in command:
                speak("Exiting voice assistant.")
                break
