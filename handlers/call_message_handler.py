from utils.speak import speak

def handle_call_message(command):
    if "call" in command:
        person = command.replace("call", "").strip()
        speak(f"Calling {person}...")
        # Implement phone call logic using Twilio or similar API if needed.
    elif "message" in command:
        person = command.replace("message", "").strip().split("to")[1]
        speak(f"Messaging {person}...")
        # Implement message sending logic with Twilio or similar API.
