import pyttsx3

# Initialize text-to-speech engine
tts_engine = pyttsx3.init()

# Function to speak out text
def speak(text):
    tts_engine.say(text)
    tts_engine.runAndWait()
