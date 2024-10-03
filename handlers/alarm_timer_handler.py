from utils.speak import speak

def handle_alarm_timer(command):
    if "alarm" in command:
        time = command.split("alarm for")[1].strip()
        speak(f"Setting alarm for {time}.")
        # Implement alarm logic
    elif "timer" in command:
        duration = command.split("timer for")[1].strip()
        speak(f"Setting a timer for {duration}.")
        # Implement timer logic
