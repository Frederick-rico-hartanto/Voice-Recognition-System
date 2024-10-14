import re
from pywinauto.application import Application
import time
from utils.speak import speak


# Functions to interact with Microsoft Clock App
def open_clock_app():
    """Open Microsoft Clock App"""
    app = Application(backend="uia").start("ms-clock:")
    time.sleep(2)
    return app


def find_timer(app, duration):
    """Check if a timer for the given duration exists, return True/False."""
    app.Clock.child_window(title="Timer", control_type="TabItem").click()
    time.sleep(1)
    all_timers = app.Clock.children(control_type="Text")
    for timer in all_timers:
        if duration in timer.window_text():
            return True
    return False


def start_timer(duration):
    """Start or create a timer for the specified duration."""
    app = open_clock_app()
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


def find_alarm(app, time_str):
    """Check if an alarm for the given time exists, return True/False."""
    app.Clock.child_window(title="Alarm", control_type="TabItem").click()
    time.sleep(1)
    all_alarms = app.Clock.children(control_type="Text")
    for alarm in all_alarms:
        if time_str in alarm.window_text():
            return True
    return False


def set_alarm(time_str):
    """Set or activate an alarm for the given time."""
    app = open_clock_app()
    if find_alarm(app, time_str):
        speak(f"Activating existing alarm for {time_str}.")
        toggle_button = app.Clock.child_window(title="Off", control_type="ToggleButton")
        toggle_button.click()
    else:
        speak(f"Creating a new alarm for {time_str}.")
        add_alarm_button = app.Clock.child_window(title="Add new alarm", control_type="Button")
        add_alarm_button.click()
        time.sleep(1)
        hours, minutes = time_str.split(":")
        app.Clock.child_window(auto_id="hours").set_text(hours)
        app.Clock.child_window(auto_id="minutes").set_text(minutes)
        save_button = app.Clock.child_window(title="Save", control_type="Button")
        save_button.click()
        time.sleep(1)
        app.Clock.child_window(title="On", control_type="ToggleButton").click()


def set_day_specific_alarm(time_str, day_of_week):
    """Set or activate an alarm for the given time on the specified day."""
    app = open_clock_app()
    if find_alarm(app, time_str):
        speak(f"Activating existing alarm for {time_str} on {day_of_week}.")
        day_button = app.Clock.child_window(title=day_of_week, control_type="CheckBox")
        if not day_button.is_checked():
            day_button.click()
    else:
        speak(f"Creating a new alarm for {time_str} on {day_of_week}.")
        add_alarm_button = app.Clock.child_window(title="Add new alarm", control_type="Button")
        add_alarm_button.click()
        time.sleep(1)
        hours, minutes = time_str.split(":")
        app.Clock.child_window(auto_id="hours").set_text(hours)
        app.Clock.child_window(auto_id="minutes").set_text(minutes)
        day_button = app.Clock.child_window(title=day_of_week, control_type="CheckBox")
        if not day_button.is_checked():
            day_button.click()
        save_button = app.Clock.child_window(title="Save", control_type="Button")
        save_button.click()
        time.sleep(1)
        app.Clock.child_window(title="On", control_type="ToggleButton").click()


# Handler function to process alarm and timer commands
def handle_alarm_timer(command):
    """Handle setting timers and alarms based on the command"""
    try:
        # Handle timers
        if "timer" in command:
            # Extract the duration from the command, e.g., "set timer for 10 minutes"
            match = re.search(r"timer\s+for\s+(\d+)\s+(minute|minutes|hour|hours)", command)
            if match:
                duration = match.group(1) + " " + match.group(2)
                speak(f"Setting a timer for {duration}.")
                start_timer(duration)
            else:
                speak("I didn't catch the duration for the timer.")

        # Handle alarms
        elif "alarm" in command:
            # Example commands: "set alarm for 7:00 AM" or "set alarm for 6:00 AM on Monday"
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
