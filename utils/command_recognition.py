import speech_recognition as sr
from speak import speak

def recognize_wake_and_command(prompt="Listening...", language="en-US"):
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        speak(prompt)
        recognizer.adjust_for_ambient_noise(source, duration=1)
        try:
            audio = recognizer.listen(source, timeout=10, phrase_time_limit=15)
        except sr.WaitTimeoutError:
            speak("I didn't hear anything. Please try again.")
            return None

    try:
        command = recognizer.recognize_google(audio, language=language)
        return command.lower()
    except sr.UnknownValueError:
        speak("Sorry, I could not understand the audio.")
        return None
    except sr.RequestError:
        speak("Sorry, there was a problem with the request.")
        return None
