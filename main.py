import re
import time
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
from handlers.currency_conversion import convert_currency  # Import currency conversion function
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


# Helper function to parse and detect conversions in natural language
def parse_conversion_command(command):
    # Match patterns like "what is 100 usd to eur", "how much is 5 kg in g"
    unit_conversion_pattern = r'what\s+is\s+(\d+)\s+([\w]+)\s+(to|in)\s+([\w]+)'
    currency_conversion_pattern = r'(how\s+much|what\s+is)\s+(\d+)\s+([\w]{3})\s+(to|in)\s+([\w]{3})'

    # Check if it matches currency conversion (prioritize currencies first)
    currency_match = re.search(currency_conversion_pattern, command, re.IGNORECASE)
    if currency_match:
        amount = float(currency_match.group(2))
        from_currency = currency_match.group(3)
        to_currency = currency_match.group(5)
        return "currency", amount, from_currency, to_currency

    # Check if it matches unit conversion
    unit_match = re.search(unit_conversion_pattern, command, re.IGNORECASE)
    if unit_match:
        amount = float(unit_match.group(1))
        from_unit = unit_match.group(2)
        to_unit = unit_match.group(4)
        return "unit", amount, from_unit, to_unit

    return None, None, None, None


# Main function to process commands
def process_command(command):
    # Normalize the command (convert to lowercase, strip spaces)
    command = command.lower().strip()

    # First, try parsing it as a potential conversion
    conversion_type, amount, from_unit, to_unit = parse_conversion_command(command)
    if conversion_type == "currency":
        # Handle currency conversion
        convert_currency(amount, from_unit, to_unit)
        return
    elif conversion_type == "unit":
        # Handle unit conversion
        handle_unit_conversion(f"convert {amount} {from_unit} to {to_unit}")
        return

    try:
        # Check if the command is translation-related
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

        # Handle opening apps
        elif "open" in command:
            app_name = command.replace("open", "").strip()
            open_app(app_name)

        # If the command is not recognized
        else:
            speak("Command not recognized.")
    except Exception as e:
        speak("An error occurred while processing the command.")
        print(f"Error: {e}")


# Main loop with wake word detection and delayed command after wake word
if __name__ == "__main__":
    wake_detected = False  # Track if wake word is detected
    last_wake_time = 0  # Track the time of the last wake word detection
    command_timeout = 60  # 1 minute to listen for a command after wake word

    try:
        while True:
            if not wake_detected:
                # Recognize wake word and full command
                command = recognize_wake_and_command(prompt="Listening for your command with wake word...")
                if command:
                    # Check if the wake word is detected
                    wake_detected, actual_command = is_wake_word_detected(command)

                    if wake_detected:
                        if actual_command:
                            # Process the actual command if it comes with the wake word
                            process_command(actual_command)
                            wake_detected = False  # Reset after processing
                        else:
                            # No command with wake word, prompt the user
                            speak("What can I help you with?")
                            last_wake_time = time.time()  # Set the time when wake word was detected
            else:
                # After wake word detected, wait for a command within the timeout period
                if time.time() - last_wake_time < command_timeout:
                    # Recognize command without wake word (since wake word already detected)
                    command = recognize_wake_and_command(prompt="Listening for your command...")

                    if command:
                        # Process the command without requiring wake word
                        process_command(command)
                        wake_detected = False  # Reset wake word detection after processing
                else:
                    # Timeout after 1 minute of waiting
                    speak("No command received. Listening for the wake word again.")
                    wake_detected = False  # Reset wake word detection

                # Exit condition
                if command and ("quit" in command or "exit" in command):
                    speak("Exiting voice assistant.")
                    break
    except KeyboardInterrupt:
        speak("Voice assistant stopped.")
    except Exception as e:
        speak("An error occurred in the main loop.")
        print(f"Main loop error: {e}")
