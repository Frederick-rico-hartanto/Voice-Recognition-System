import re
from pywinauto.application import Application
from pywinauto.findwindows import find_windows
import time
from utils.speak import speak
import subprocess


def open_clock_app():
    """Open Microsoft Clock App using subprocess and log control identifiers."""
    try:
        print("[DEBUG] Attempting to open Clock app")
        # Open the Clock App using subprocess
        subprocess.Popen(["start", "ms-clock:"], shell=True)
        time.sleep(3)  # Give some time for the app to open

        # Attach to the running Clock app
        app = Application(backend="uia").connect(title_re="Clock")
        print("[DEBUG] Clock app opened successfully")

        # Log control identifiers to investigate the structure
        app.Clock.print_control_identifiers()
        return app
    except Exception as e:
        speak(f"Failed to open the Clock app: {e}")
        print(f"[ERROR] Error opening the Clock app: {e}")
        return None


def find_timer(app, duration):
    """Check if a timer for the given duration exists, return True/False."""
    try:
        print(f"[DEBUG] Checking for existing timer for {duration}")
        app.Clock.child_window(title="Timer", control_type="TabItem").click()
        time.sleep(1)
        all_timers = app.Clock.children(control_type="Text")
        for timer in all_timers:
            if duration in timer.window_text():
                print(f"[DEBUG] Timer for {duration} found")
                return True
        print(f"[DEBUG] No timer found for {duration}")
        return False
    except Exception as e:
        print(f"[ERROR] Error finding timer: {e}")
        return False


def start_timer(duration):
    """Start or create a timer for the specified duration."""
    try:
        print(f"[DEBUG] Starting timer for {duration}")
        app = open_clock_app()
        if app is None:
            return  # Exit if clock app fails to open
        if find_timer(app, duration):
            speak(f"Activating existing timer for {duration}.")
            play_button = app.Clock.child_window(title="Play", control_type="Button")
            play_button.click()
        else:
            speak(f"Creating a new timer for {duration}.")
            add_timer_button = app.Clock.child_window(title="Add new timer", control_type="Button")
            add_timer_button.click()
            time.sleep(1)
            app.Clock.child_window(auto_id="hours").set_text("0")
            app.Clock.child_window(auto_id="minutes").set_text("1" if duration == "1 minute" else duration.split()[0])
            save_button = app.Clock.child_window(title="Save", control_type="Button")
            save_button.click()
            time.sleep(1)
            app.Clock.child_window(title="Play", control_type="Button").click()
        print("[DEBUG] Timer started successfully")
    except Exception as e:
        print(f"[ERROR] Error starting timer: {e}")


def find_alarm(app, time_str):
    """Check if an alarm for the given time exists, return True/False."""
    try:
        print(f"[DEBUG] Checking for existing alarm for {time_str}")
        app.Clock.child_window(title="Alarm", control_type="ListItem").click()
        time.sleep(2)  # Allow some time for the UI to load
        all_alarms = app.Clock.children(control_type="Text")
        for alarm in all_alarms:
            if time_str in alarm.window_text():
                print(f"[DEBUG] Alarm for {time_str} found")
                return True
        print(f"[DEBUG] No alarm found for {time_str}")
        return False
    except Exception as e:
        print(f"[ERROR] Error finding alarm: {e}")
        return False


def set_alarm(time_str):
    """Set or activate an alarm for the given time."""
    try:
        print(f"[DEBUG] Setting alarm for {time_str}")
        app = open_clock_app()
        if app is None:
            return  # Exit if clock app fails to open

        if find_alarm(app, time_str):
            speak(f"Activating existing alarm for {time_str}.")
            toggle_button = app.Clock.child_window(title="Off", control_type="ToggleButton")
            if toggle_button.exists():
                toggle_button.click()
            else:
                print(f"[ERROR] Unable to find 'Off' toggle button for alarm.")
        else:
            speak(f"Creating a new alarm for {time_str}.")
            # Find and click the 'Add new alarm' button
            add_alarm_button = app.Clock.child_window(title="Add new alarm", control_type="Button")

            # Retry if the button is not immediately found
            retries = 5
            while not add_alarm_button.exists() and retries > 0:
                print("[DEBUG] Waiting for 'Add new alarm' button to appear...")
                time.sleep(1)
                retries -= 1

            if add_alarm_button.exists():
                add_alarm_button.click()
                time.sleep(2)

                # Set the hours and minutes
                hours, minutes = time_str.split(":")
                app.Clock.child_window(auto_id="hours").set_text(hours)
                app.Clock.child_window(auto_id="minutes").set_text(minutes)

                # Save the alarm
                save_button = app.Clock.child_window(title="Save", control_type="Button")
                save_button.click()
                time.sleep(2)

                # Toggle the alarm to "On"
                app.Clock.child_window(title="On", control_type="ToggleButton").click()
                print("[DEBUG] Alarm set successfully")
            else:
                print(f"[ERROR] 'Add new alarm' button not found.")
    except Exception as e:
        print(f"[ERROR] Error setting alarm: {e}")


def set_day_specific_alarm(time_str, day_of_week):
    """Set or activate an alarm for the given time on the specified day."""
    try:
        print(f"[DEBUG] Setting day-specific alarm for {time_str} on {day_of_week}")
        app = open_clock_app()
        if app is None:
            return  # Exit if clock app fails to open

        if find_alarm(app, time_str):
            speak(f"Activating existing alarm for {time_str} on {day_of_week}.")
            day_button = app.Clock.child_window(title=day_of_week, control_type="CheckBox")
            if not day_button.is_checked():
                day_button.click()
        else:
            speak(f"Creating a new alarm for {time_str} on {day_of_week}.")
            add_alarm_button = app.Clock.child_window(title="Add new alarm", control_type="Button")

            # Retry if the button is not immediately found
            retries = 5
            while not add_alarm_button.exists() and retries > 0:
                print("[DEBUG] Waiting for 'Add new alarm' button to appear...")
                time.sleep(1)
                retries -= 1

            if add_alarm_button.exists():
                add_alarm_button.click()
                time.sleep(2)

                # Set the hours and minutes
                hours, minutes = time_str.split(":")
                app.Clock.child_window(auto_id="hours").set_text(hours)
                app.Clock.child_window(auto_id="minutes").set_text(minutes)

                # Select the day of the week
                day_button = app.Clock.child_window(title=day_of_week, control_type="CheckBox")
                if not day_button.is_checked():
                    day_button.click()

                # Save the alarm
                save_button = app.Clock.child_window(title="Save", control_type="Button")
                save_button.click()
                time.sleep(2)

                # Toggle the alarm to "On"
                app.Clock.child_window(title="On", control_type="ToggleButton").click()
                print("[DEBUG] Day-specific alarm set successfully")
            else:
                print(f"[ERROR] 'Add new alarm' button not found.")
    except Exception as e:
        print(f"[ERROR] Error setting day-specific alarm: {e}")

# Handler function to process alarm and timer commands
def handle_alarm_timer(command):
    """Handle setting timers and alarms based on the command"""
    try:
        print(f"[DEBUG] Processing command: {command}")
        app = open_clock_app()  # Open the app and log control identifiers
        if app is None:
            return  # Exit if the app failed to open

        # Handle alarms
        if "alarm" in command:
            time_match = re.search(r"alarm\s+for\s+(\d+:\d+)", command)
            day_match = re.search(r"on\s+(monday|tuesday|wednesday|thursday|friday|saturday|sunday)", command,
                                  re.IGNORECASE)

            if time_match:
                time_str = time_match.group(1)
                if day_match:
                    day_of_week = day_match.group(1).capitalize()
                    speak(f"Setting an alarm for {time_str} on {day_of_week}.")
                    set_day_specific_alarm(time_str, day_of_week)
                else:
                    speak(f"Setting an alarm for {time_str}.")
                    set_alarm(time_str)
            else:
                speak("I didn't catch the time for the alarm.")

        else:
            speak("I didn't understand if you wanted to set a timer or an alarm.")

    except Exception as e:
        speak(f"An error occurred while handling the timer or alarm: {e}")
        print(f"[ERROR] Error handling alarm/timer: {e}")

# Add this block to run the test
if __name__ == "__main__":
    # Example test command for setting a timer or alarm
    test_command = "set timer 1 minute"  # You can change this command for testing
    print(f"[DEBUG] Running test with command: {test_command}")
    handle_alarm_timer(test_command)
