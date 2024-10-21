import subprocess
from utils.speak import speak  # Assuming `speak` is a TTS (Text-to-Speech) function
import re

def handle_alarm_timer(command):
    """
    Handles commands related to timers, alarms, and stopwatches by calling the appropriate C# function.
    """
    print(f"Received command: {command}")
    
    if "timer" in command:
        # Extract timer duration (minutes, hours, or seconds) from the command using regular expressions
        duration = convert_command_to_duration(command)
        if duration:
            human_friendly_duration = format_duration_for_speech(duration)
            print(f"Setting timer for {human_friendly_duration}.")
            speak(f"Setting a timer for {human_friendly_duration}.")
            set_timer_via_csharp(duration)  # Processing internally as h:m:s format
        else:
            print("Failed to parse timer duration.")
            speak("I couldn't understand the timer duration.")
    
    elif "alarm" in command:
        # Extract alarm time from the command using regular expressions
        alarm_match = re.search(r'(\d{1,2}:\d{2})', command)
        if alarm_match:
            alarm_time = alarm_match.group(1)
            print(f"Setting alarm for {alarm_time}.")
            speak(f"Setting an alarm for {alarm_time}.")
            set_alarm_via_csharp(alarm_time)
        else:
            print("Failed to parse alarm time.")
            speak("I couldn't understand the alarm time.")

    elif "stopwatch" in command:
        if "start" in command:
            speak("Starting the stopwatch.")
            set_stopwatch_via_csharp("start")
        elif "pause" in command:
            speak("Pausing the stopwatch.")
            set_stopwatch_via_csharp("pause")
        elif "reset" in command:
            speak("Resetting the stopwatch.")
            set_stopwatch_via_csharp("reset")
        else:
            speak("I couldn't understand the stopwatch command.")

def convert_command_to_duration(command):
    """
    Converts a spoken command like '1 minute', '30 seconds' or '1 hour' to '0:1:0', '0:0:30', or '1:0:0' (h:m:s format).
    """
    hours = 0
    minutes = 0
    seconds = 0

    # Check for hours in the command
    hours_match = re.search(r'(\d+)\s*hour', command)
    if hours_match:
        hours = int(hours_match.group(1))

    # Check for minutes in the command
    minutes_match = re.search(r'(\d+)\s*minute', command)
    if minutes_match:
        minutes = int(minutes_match.group(1))

    # Check for seconds in the command
    seconds_match = re.search(r'(\d+)\s*second', command)
    if seconds_match:
        seconds = int(seconds_match.group(1))

    # If no time units found, return None (failed parsing)
    if hours == 0 and minutes == 0 and seconds == 0:
        return None

    # Return the formatted duration in "h:m:s" format
    return f"{hours}:{minutes}:{seconds}"

def format_duration_for_speech(duration):
    """
    Converts duration in h:m:s format (e.g., '0:1:0') into human-friendly speech format (e.g., '1 minute').
    """
    parts = duration.split(':')
    hours = int(parts[0])
    minutes = int(parts[1])
    seconds = int(parts[2])

    # Create human-friendly parts
    human_parts = []
    if hours == 1:
        human_parts.append(f"{hours} hour")
    elif hours > 1:
        human_parts.append(f"{hours} hours")

    if minutes == 1:
        human_parts.append(f"{minutes} minute")
    elif minutes > 1:
        human_parts.append(f"{minutes} minutes")

    if seconds == 1:
        human_parts.append(f"{seconds} second")
    elif seconds > 1:
        human_parts.append(f"{seconds} seconds")

    # Join parts with commas and 'and'
    if len(human_parts) == 0:
        return "0 seconds"  # Edge case where no time was parsed
    elif len(human_parts) == 1:
        return human_parts[0]  # Only one part (e.g., "1 minute")
    else:
        return ', '.join(human_parts[:-1]) + f" and {human_parts[-1]}"

def set_timer_via_csharp(duration):
    """
    Function to invoke the C# ClockAutomation executable to set a timer with a specified duration.
    """
    try:
        # Debug: print duration before invoking
        print(f"Invoking C# automation for timer with duration: {duration} (h:m:s).")

        # Call the C# executable with timer duration (replace with actual path)
        result = subprocess.run(["cs_code/ClockAutomation/bin/Debug/net48/ClockAutomation.exe", "timer", str(duration)], capture_output=True, text=True)
        
        # Print the output from the C# process (if any)
        print(result.stdout)

        # Check for errors in execution
        if result.returncode != 0:
            print(f"[ERROR] Error setting timer via C#: {result.stderr}")
            speak("There was an error setting the timer.")
        else:
            print(f"[INFO] Timer for {duration} set successfully via C#.")
            speak(f"Timer set successfully.")
    
    except Exception as e:
        print(f"[ERROR] Failed to call C# executable: {e}")
        speak("I could not set the timer due to an error.")

def set_alarm_via_csharp(alarm_time):
    """
    Function to invoke the C# ClockAutomation executable to set an alarm at a specified time.
    """
    try:
        # Path to the C# executable (ensure the path is correct based on your project structure)
        executable_path = "cs_code/ClockAutomation/bin/Debug/net48/ClockAutomation.exe"
        
        # Call the C# executable with "alarm" argument and the time
        result = subprocess.run([executable_path, "alarm", str(alarm_time)], capture_output=True, text=True)

        # Print the output from the C# process (if any)
        print(result.stdout)

        # Check for errors in execution
        if result.returncode != 0:
            print(f"[ERROR] Error setting alarm via C#: {result.stderr}")
            speak("There was an error setting the alarm.")
        else:
            print(f"[INFO] Alarm set successfully for {alarm_time} via C#.")
            speak(f"Alarm set for {alarm_time}.")
    
    except FileNotFoundError:
        print(f"[ERROR] C# executable not found at {executable_path}.")
        speak("I couldn't find the alarm application to set the alarm.")
    except Exception as e:
        print(f"[ERROR] Failed to call C# executable: {e}")
        speak("I could not set the alarm due to an error.")

def set_stopwatch_via_csharp(action):
    """
    Function to invoke the C# ClockAutomation executable to start, pause, or reset the stopwatch.
    """
    try:
        # Path to the C# executable (ensure the path is correct based on your project structure)
        executable_path = "cs_code/ClockAutomation/bin/Debug/net48/ClockAutomation.exe"

        # Call the C# executable with "stopwatch" argument and the action (start, pause, or reset)
        result = subprocess.run([executable_path, "stopwatch", action], capture_output=True, text=True)

        # Print the output from the C# process (if any)
        print(result.stdout)

        # Check for errors in execution
        if result.returncode != 0:
            print(f"[ERROR] Error controlling stopwatch via C#: {result.stderr}")
            speak(f"There was an error while trying to {action} the stopwatch.")
        else:
            print(f"[INFO] Stopwatch {action} successfully via C#.")
            speak(f"Stopwatch {action} successfully.")
    
    except FileNotFoundError:
        print(f"[ERROR] C# executable not found at {executable_path}.")
        speak("I couldn't find the stopwatch application to perform the action.")
    except Exception as e:
        print(f"[ERROR] Failed to call C# executable: {e}")
        speak("I could not control the stopwatch due to an error.")
