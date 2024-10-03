from googletrans import Translator
from utils.speak import speak

# Function to extract the phrase and language for translation
def extract_translation(command):
    parts = command.split("in")
    if len(parts) == 2:
        phrase = parts[0].replace("translate", "").replace("what is", "").strip()
        lang = parts[1].strip()
        return phrase, lang
    return command, 'en'

# Function to translate a given phrase using googletrans
def translate_phrase(phrase, lang='en'):
    translator = Translator()
    try:
        translated = translator.translate(phrase, dest=lang)
        print(f"Translation: {translated.text}")
        speak(f"Translation: {translated.text}")
        return translated.text
    except Exception as e:
        print(f"Error translating phrase: {e}")
        speak("Error translating the phrase")
        return None
