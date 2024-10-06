from googletrans import Translator
from utils.speak import speak

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


# Improved function to extract the phrase and language for translation
def extract_translation(command):
    command = command.lower().strip()  # Normalize case and strip leading/trailing spaces

    # Check for keywords like "translate" or "what is"
    if "translate" in command:
        command = command.replace("translate", "").strip()
    if "what is" in command:
        command = command.replace("what is", "").strip()

    # Split the phrase from the language using "in"
    if " in " in command:
        parts = command.split(" in ")
        phrase = parts[0].strip()
        lang = parts[1].strip().lower()

        # Map the language to a language code (if possible)
        lang_code = language_map.get(lang, lang)
        return phrase, lang_code
    else:
        # If "in" is missing, assume English as the target language
        return command, 'en'

# Function to translate a given phrase using googletrans
def translate_phrase(phrase, lang='en'):
    translator = Translator()
    try:
        # Perform translation using googletrans
        translated = translator.translate(phrase, dest=lang)
        print(f"Translation: {translated.text}")
        speak(f"Translation: {translated.text}")
        return translated.text
    except Exception as e:
        print(f"Error translating phrase: {e}")
        speak("Error translating the phrase. Please check your network or the language code.")
        return None