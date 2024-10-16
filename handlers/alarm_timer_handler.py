import subprocess
from utils.speak import speak
import re

def handle_alarm_timer(command):
    """
    Handles commands related to timers and alarms by calling the appropriate C# function.
    """
    if "timer" in command:
        # Extract timer duration from the command using regular expressions
        duration_match = re.search(r'(\d+) minute', command)
        if duration_match:
            duration = int(duration_match.group(1))
            speak(f"Setting a timer for {duration} minutes.")
            set_timer_via_csharp(duration)
        else:
            speak("I couldn't understand the timer duration.")

    elif "alarm" in command:
        # Extract alarm time from the command using regular expressions
        alarm_match = re.search(r'(\d{1,2}:\d{2})', command)
        if alarm_match:
            alarm_time = alarm_match.group(1)
            speak(f"Setting an alarm for {alarm_time}.")
            set_alarm_via_csharp(alarm_time)
        else:
            speak("I couldn't understand the alarm time.")

def set_timer_via_csharp(duration):
    """
    Function to invoke the C# ClockAutomation executable to set a timer with a specified duration.
    """
    try:
        # Call the C# executable with timer duration (replace with actual path)
        result = subprocess.run(["cs_code/ClockAutomation.exe", "timer", str(duration)], capture_output=True, text=True)
        
        # Print the output from the C# process (if any)
        print(result.stdout)
        speak(result.stdout)

        # Check for errors in execution
        if result.returncode != 0:
            print(f"[ERROR] Error setting timer via C#: {result.stderr}")
            speak("There was an error setting the timer.")
        else:
            print(f"[INFO] Timer for {duration} minutes set successfully via C#.")
            speak(f"Timer set for {duration} minutes.")
    
    except Exception as e:
        print(f"[ERROR] Failed to call C# executable: {e}")
        speak("I could not set the timer due to an error.")

def set_alarm_via_csharp(alarm_time):
    """
    Function to invoke the C# ClockAutomation executable to set an alarm at a specified time.
    """
    try:
        # Call the C# executable with alarm time (replace with actual path)
        result = subprocess.run(["cs_code/ClockAutomation.exe", "alarm", str(alarm_time)], capture_output=True, text=True)

        # Print the output from the C# process (if any)
        print(result.stdout)
        speak(result.stdout)

        # Check for errors in execution
        if result.returncode != 0:
            print(f"[ERROR] Error setting alarm via C#: {result.stderr}")
            speak("There was an error setting the alarm.")
        else:
            print(f"[INFO] Alarm set successfully for {alarm_time} via C#.")
            speak(f"Alarm set for {alarm_time}.")
    
    except Exception as e:
        print(f"[ERROR] Failed to call C# executable: {e}")
        speak("I could not set the alarm due to an error.")

# MAIN FUNCTION TO RUN THE SCRIPT
def main():
    # Example test command for setting a timer or alarm
    test_command = "set alarm for 7:00 AM on Monday"  # Change this for different tests
    print(f"[DEBUG] Running test with command: {test_command}")
    
    handle_alarm_timer(test_command)

if __name__ == "__main__":
    main()
