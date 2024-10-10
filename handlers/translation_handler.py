from googletrans import Translator
from gtts import gTTS
import os
import pygame
from utils.speak import speak
import re

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
    'chinese': 'zh-cn',  # Default to Simplified Chinese
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

# Initialize pygame for sound playing
pygame.mixer.init()

# Improved function to extract the phrase and language for translation
def extract_translation(command):
    command = command.lower().strip()  # Normalize case and strip leading/trailing spaces

    # Regex patterns to handle various translation phrases
    translation_patterns = [
        r"translate\s+(.+?)\s+to\s+(.+)",  # Translate X to Y
        r"what\s+is\s+(.+?)\s+in\s+(.+)",  # What is X in Y
        r"how\s+do\s+you\s+say\s+(.+?)\s+in\s+(.+)"  # How do you say X in Y
    ]

    for pattern in translation_patterns:
        match = re.search(pattern, command, re.IGNORECASE)
        if match:
            phrase = match.group(1).strip()
            lang = match.group(2).strip().lower()
            # Map the language to a language code (if possible)
            lang_code = language_map.get(lang, lang)
            return phrase, lang_code

    # Fallback if no match found
    return command, 'en'  # Default to English if no specific language is found


# Function to ensure pygame mixer is initialized
def init_pygame_mixer():
    if not pygame.mixer.get_init():
        pygame.mixer.init()

# Function to translate and pronounce a given phrase using googletrans and gTTS
def translate_phrase(phrase, lang='en'):
    translator = Translator()
    try:
        # Perform translation using googletrans
        translated = translator.translate(phrase, dest=lang)
        translated_text = translated.text
        print(f"Translation: {translated_text}")
        speak(f"Translation: {translated_text}")

        # Pronounce the translated text in the respective language using gTTS
        tts = gTTS(text=translated_text, lang=lang)
        tts.save("translated_speech.mp3")

        # Ensure pygame mixer is initialized before trying to play audio
        init_pygame_mixer()

        # Play the saved audio file using pygame
        pygame.mixer.music.load("translated_speech.mp3")
        pygame.mixer.music.play()

        # Wait for the sound to finish playing and ensure pygame releases the file
        while pygame.mixer.music.get_busy():
            continue

        # Stop the mixer and release resources
        pygame.mixer.music.stop()

        # Retry deleting the file after ensuring no process is using it
        if os.path.exists("translated_speech.mp3"):
            try:
                os.remove("translated_speech.mp3")
            except PermissionError:
                print("File is still in use. Retrying deletion in 2 seconds.")
                pygame.time.wait(2000)  # Wait 2 seconds before trying again
                os.remove("translated_speech.mp3")

        return translated_text

    except Exception as e:
        print(f"Error translating or pronouncing phrase: {e}")
        speak("Error translating or pronouncing the phrase. Please check your network or the language code.")
        return None