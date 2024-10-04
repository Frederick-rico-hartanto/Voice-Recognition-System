from utils.speak import speak
from utils.command_recognition import recognize_wake_and_command, is_time_related, is_date_related, is_search_related, \
    is_translation_related, is_math_related
from handlers.email_handler import handle_email
from handlers.call_message_handler import handle_call_message
from handlers.calendar_reminder_handler import handle_reminder_or_calendar
from handlers.alarm_timer_handler import handle_alarm_timer
from handlers.notes_list_handler import handle_notes_or_lists
from handlers.weather_handler import handle_weather
from handlers.unit_conversion_handler import handle_unit_conversion
from utils.time_date_handler import handle_time_command, handle_date_command
from handlers.search_handler import search_online
from handlers.translation_handler import translate_phrase, extract_translation
from handlers.open_apps import open_app
from utils.math_solver import extract_equation, solve_math_equation


# Function to check for wake word in the command
def is_wake_word_detected(command):
    wake_words = ["hey bella", "okay bella"]
    for wake_word in wake_words:
        if command.startswith(wake_word):
            return True, command.replace(wake_word, "").strip()  # Remove the wake word from command
    return False, None


def process_command(command):
    # Check if the command is translation-related first to prioritize translations over searches
    if is_translation_related(command):
        phrase, lang = extract_translation(command)
        translate_phrase(phrase, lang)

    # Handle calling or messaging tasks
    elif "call" in command or "message" in command:
        handle_call_message(command)

    # Handle email
    elif "email" in command:
        handle_email(command)

    # Handle reminders or calendar
    elif "reminder" in command or "calendar" in command:
        handle_reminder_or_calendar(command)

    # Handle alarms or timers
    elif "alarm" in command or "timer" in command:
        handle_alarm_timer(command)

    # Handle notes or lists
    elif "note" in command or "list" in command:
        handle_notes_or_lists(command)

    # Handle weather
    elif "weather" in command:
        handle_weather(command)

    # Handle unit conversion
    elif "convert" in command:
        handle_unit_conversion(command)

    # Handle math-related commands
    elif is_math_related(command):
        equation = extract_equation(command)
        solve_math_equation(equation)

    # Handle time-related commands
    elif is_time_related(command):
        handle_time_command(command)

    # Handle date-related commands
    elif is_date_related(command):
        handle_date_command(command)

    # Handle search-related commands (should come last, after translation is checked)
    elif is_search_related(command):
        search_online(command)

    elif "open" in command:
        app_name = command.replace("open", "").strip()
        open_app(app_name)  # Open any app

    # If the command is not recognized
    else:
        speak("Command not recognized.")


# Main loop with wake word detection
if __name__ == "__main__":
    while True:
        # Recognize wake word and full command
        command = recognize_wake_and_command(prompt="Listening for your command with wake word...")
        if command:
            # Check if the wake word is detected
            wake_detected, actual_command = is_wake_word_detected(command)
            if wake_detected:
                # Process the actual command without the wake word
                process_command(actual_command)
            else:
                speak("Please start with 'Hey Bella' or 'Okay Bella'.")

            # Exit condition
            if "quit" in command or "exit" in command:
                speak("Exiting voice assistant.")
                break
