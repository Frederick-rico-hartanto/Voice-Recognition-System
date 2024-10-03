from datetime import datetime, timedelta
from utils.speak import speak

# Function to handle time-related commands
def handle_time_command(command):
    current_time = datetime.now().strftime("%I:%M %p")  # 12-hour format with AM/PM
    print(f"The current time is {current_time}")
    speak(f"The current time is {current_time}")

# Function to handle date-related commands
def handle_date_command(command):
    if 'tomorrow' in command:
        date = (datetime.now() + timedelta(days=1)).strftime("%A, %B %d, %Y")
        print(f"Tomorrow's date is {date}")
        speak(f"Tomorrow's date is {date}")
    elif 'yesterday' in command:
        date = (datetime.now() - timedelta(days=1)).strftime("%A, %B %d, %Y")
        print(f"Yesterday's date was {date}")
        speak(f"Yesterday's date was {date}")
    else:
        date = datetime.now().strftime("%A, %B %d, %Y")  # Get today's date
        print(f"Today's date is {date}")
        speak(f"Today's date is {date}")
