import re
from googletrans import Translator
from gtts import gTTS
import os
import pygame
import time  # Make sure this is imported
from utils.speak import speak
from gtts.lang import tts_langs

# Print available languages for gTTS for reference
available_gtts_langs = tts_langs()
print("Available gTTS languages:", available_gtts_langs)

# Initialize pygame for sound playing
pygame.mixer.init()

# Complete list of Google Translate supported language codes mapped to common language names
language_map = {
    'af': 'af',  # Afrikaans
    'albanian': 'sq',
    'arabic': 'ar',
    'armenian': 'hy',
    'azerbaijani': 'az',
    'basque': 'eu',
    'belarusian': 'be',
    'bengali': 'bn',
    'bosnian': 'bs',
    'bulgarian': 'bg',
    'catalan': 'ca',
    'cebuano': 'ceb',
    'mandarin': 'zh-cn',  # Simplified Chinese (Mandarin)
    'simplified chinese': 'zh-cn',
    'traditional chinese': 'zh-tw',
    'chinese': 'zh-cn',  # Default to Simplified Chinese for Google Translate
    'corsican': 'co',
    'croatian': 'hr',
    'czech': 'cs',
    'danish': 'da',
    'dutch': 'nl',
    'english': 'en',
    'esperanto': 'eo',
    'estonian': 'et',
    'finnish': 'fi',
    'french': 'fr',
    'frisian': 'fy',
    'galician': 'gl',
    'georgian': 'ka',
    'german': 'de',
    'greek': 'el',
    'gujarati': 'gu',
    'haitian creole': 'ht',
    'hausa': 'ha',
    'hawaiian': 'haw',
    'hebrew': 'he',
    'hindi': 'hi',
    'hmong': 'hmn',
    'hungarian': 'hu',
    'icelandic': 'is',
    'igbo': 'ig',
    'indonesian': 'id',
    'irish': 'ga',
    'italian': 'it',
    'japanese': 'ja',
    'javanese': 'jw',
    'kannada': 'kn',
    'kazakh': 'kk',
    'khmer': 'km',
    'korean': 'ko',
    'kurdish': 'ku',
    'kyrgyz': 'ky',
    'lao': 'lo',
    'latin': 'la',
    'latvian': 'lv',
    'lithuanian': 'lt',
    'luxembourgish': 'lb',
    'macedonian': 'mk',
    'malagasy': 'mg',
    'malay': 'ms',
    'malayalam': 'ml',
    'maltese': 'mt',
    'maori': 'mi',
    'marathi': 'mr',
    'mongolian': 'mn',
    'myanmar': 'my',  # Burmese
    'nepali': 'ne',
    'norwegian': 'no',
    'nyanja': 'ny',  # Chichewa
    'odia': 'or',  # Oriya
    'pashto': 'ps',
    'persian': 'fa',
    'polish': 'pl',
    'portuguese': 'pt',
    'punjabi': 'pa',
    'romanian': 'ro',
    'russian': 'ru',
    'samoan': 'sm',
    'scots gaelic': 'gd',
    'serbian': 'sr',
    'sesotho': 'st',
    'shona': 'sn',
    'sindhi': 'sd',
    'sinhala': 'si',  # Sinhalese
    'slovak': 'sk',
    'slovenian': 'sl',
    'somali': 'so',
    'spanish': 'es',
    'sundanese': 'su',
    'swahili': 'sw',
    'swedish': 'sv',
    'tagalog': 'tl',  # Filipino
    'tajik': 'tg',
    'tamil': 'ta',
    'telugu': 'te',
    'thai': 'th',
    'turkish': 'tr',
    'ukrainian': 'uk',
    'urdu': 'ur',
    'uzbek': 'uz',
    'vietnamese': 'vi',
    'welsh': 'cy',
    'xhosa': 'xh',
    'yiddish': 'yi',
    'yoruba': 'yo',
    'zulu': 'zu',
}

# Function to extract the phrase and language for translation
def extract_translation(command):
    command = command.lower().strip()  # Normalize case and strip leading/trailing spaces
    print(f"Command received: {command}")  # Debugging statement

    # Regex patterns to handle various translation phrases
    translation_patterns = [
        r"translate\s+(.+?)\s+to\s+(.+)",  # Translate X to Y
        r"translate\s+(.+?)\s+in\s+(.+)",  # Translate X in Y
        r"what\s+is\s+(.+?)\s+in\s+(.+)",  # What is X in Y
        r"how\s+do\s+you\s+say\s+(.+?)\s+in\s+(.+)"  # How do you say X in Y
    ]

    for pattern in translation_patterns:
        match = re.search(pattern, command, re.IGNORECASE)
        if match:
            phrase = match.group(1).strip()
            lang = match.group(2).strip().lower()
            print(f"Matched phrase: {phrase}, language: {lang}")  # Debugging statement
            # Map the language to a language code (if possible)
            lang_code = language_map.get(lang, lang)
            print(f"Language code: {lang_code}")  # Debugging statement
            return phrase, lang_code

    # Fallback if no match found
    print("No matching pattern found.")  # Debugging statement
    return None, None  # Return None if no valid pattern is found

# Function to translate and pronounce a given phrase using googletrans and gTTS
def translate_phrase(phrase, lang):
    translator = Translator()
    try:
        # Convert language codes between Google Translate and gTTS if necessary
        gtts_lang = lang
        if lang == 'zh-cn':
            gtts_lang = 'zh'  # Simplified Chinese for gTTS
        elif lang == 'zh-tw':
            gtts_lang = 'zh-tw'  # Traditional Chinese for gTTS

        # Perform translation using googletrans
        translated = translator.translate(phrase, dest=lang)
        translated_text = translated.text
        print(f"Translation: {translated_text}")
        speak(f"Translation: {translated_text}")

        # Pronounce the translated text in the respective language using gTTS
        if gtts_lang not in available_gtts_langs:
            print(f"Language '{gtts_lang}' is not supported by gTTS. Falling back to English.")
            speak(f"Sorry, pronunciation in {gtts_lang} is not available.")
            return translated_text

        tts = gTTS(text=translated_text, lang=gtts_lang)

        # Check if gTTS supports the language
        print(f"Language code for gTTS: {gtts_lang}")

        # Save the mp3 file
        tts.save("translated_speech.mp3")

        # Ensure pygame mixer is initialized before trying to play audio
        if init_pygame_mixer():
            # Play the saved audio file using pygame
            pygame.mixer.music.load("translated_speech.mp3")
            pygame.mixer.music.play()

            # Wait for the sound to finish playing and ensure pygame releases the file
            while pygame.mixer.music.get_busy():
                time.sleep(0.1)

            # Stop the mixer and quit pygame to release resources
            pygame.mixer.music.stop()
            pygame.mixer.quit()

            # Now it's safe to delete the file after the mixer has stopped
            if os.path.exists("translated_speech.mp3"):
                os.remove("translated_speech.mp3")
        else:
            print("Error: pygame mixer could not be initialized.")
            speak("Sorry, I cannot play the audio right now.")
        return translated_text

    except Exception as e:
        print(f"Error translating or pronouncing phrase: {e}")
        speak("Error translating or pronouncing the phrase. Please check your network or the language code.")
        return None

# Function to ensure pygame mixer is initialized
def init_pygame_mixer():
    if not pygame.mixer.get_init():
        try:
            pygame.mixer.init()
            print("pygame mixer initialized successfully.")
        except Exception as mixer_error:
            print(f"Error initializing pygame mixer: {mixer_error}")
            return False
    return True
