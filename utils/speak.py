import pyttsx3
from gtts import gTTS
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


# Main function to decide which TTS engine to use based on the language
def speak(text, lang='en'):
    # Use gTTS for non-Latin languages (Chinese, Japanese, etc.)
    if lang in ['zh-cn', 'zh-tw', 'ja', 'ko']:  # Mandarin, Traditional Chinese, Japanese, Korean
        speak_multilingual(text, lang)
    else:
        # Use pyttsx3 for Latin-based languages
        pyttsx_speak(text)


# Example usage
if __name__ == "__main__":
    # Test with Simplified Chinese (handled by gTTS)
    speak("你好", lang='zh-cn')

    # Test with Japanese (handled by gTTS)
    speak("こんにちは", lang='ja')

    # Test with English (handled by pyttsx3)
    speak("Hello, how are you?", lang='en')
