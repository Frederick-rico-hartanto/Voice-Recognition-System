import pyttsx3
from gtts import gTTS
from googletrans import Translator
import os
import io
import pygame

# Initialize pyttsx3 TTS engine for Latin-based languages
tts_engine = pyttsx3.init()

# Initialize pygame mixer for audio playback
pygame.mixer.init()

# Function to use pyttsx3 for speaking Latin-based languages
def pyttsx_speak(text):
    try:
        tts_engine.say(text)
        tts_engine.runAndWait()
    except Exception as e:
        print(f"Error with pyttsx3 TTS: {e}")

# Function to use gTTS for speaking non-Latin languages (like Chinese, Japanese)
def speak_multilingual(text, lang='en'):
    try:
        # Use gTTS to convert text to speech and store it in a BytesIO buffer
        tts = gTTS(text=text, lang=lang)
        fp = io.BytesIO()
        tts.write_to_fp(fp)
        fp.seek(0)  # Move the pointer to the beginning of the BytesIO stream

        # Play the audio using pygame (from memory)
        pygame.mixer.music.load(fp, 'mp3')
        pygame.mixer.music.play()

        while pygame.mixer.music.get_busy():  # Wait for the speech to finish
            pass

    except Exception as e:
        print(f"Error with gTTS: {e}")
        pyttsx_speak("Sorry, I can't pronounce that.")

# Function to translate text to the desired language using googletrans
def translate_phrase(phrase, lang='en'):
    translator = Translator()
    try:
        # Perform the translation
        translated = translator.translate(phrase, dest=lang)
        return translated.text  # Removed print statement
    except Exception as e:
        print(f"Error translating phrase: {e}")
        return phrase  # In case of failure, return the original phrase

# Main function to handle translation and speaking
def speak(text, target_language_code='en'):
    # First, translate the text into the target language
    translated_text = translate_phrase(text, target_language_code)

    # Next, speak the translated text based on the language
    if target_language_code in ['zh-cn', 'zh-tw', 'ja', 'ko']:  # Non-Latin languages
        speak_multilingual(translated_text, target_language_code)
    else:
        pyttsx_speak(translated_text)  # Latin-based languages use pyttsx3

# Example usage
if __name__ == "__main__":
    # Translate and speak in Simplified Chinese (Mandarin)
    speak("Hello, how are you?", 'zh-cn')

    # Translate and speak in Japanese
    speak("Good morning", 'ja')

    # Translate and speak in Korean
    speak("Thank you", 'ko')

    # Translate and speak in English (Latin-based language, will use pyttsx3)
    speak("Good afternoon", 'en')
