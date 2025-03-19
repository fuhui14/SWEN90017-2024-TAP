import deepl
from config.settings import auth_key

LANGUAGE_MAP = {
    "Bulgarian": "BG", "Czech": "CS", "Danish": "DA", "German": "DE", "Greek": "EL",
    "English": "EN", "Spanish": "ES", "Estonian": "ET", "Finnish": "FI", "French": "FR",
    "Hungarian": "HU", "Indonesian": "ID", "Italian": "IT", "Japanese": "JA", "Korean": "KO",
    "Lithuanian": "LT", "Latvian": "LV", "Norwegian": "NB", "Dutch": "NL", "Polish": "PL",
    "Portuguese": "PT", "Romanian": "RO", "Russian": "RU", "Slovak": "SK", "Slovenian": "SL",
    "Swedish": "SV", "Turkish": "TR", "Ukrainian": "UK", "Chinese": "ZH"
}


def translate(text, lang_code):
    if lang_code.capitalize() in LANGUAGE_MAP:
        lang_code = LANGUAGE_MAP[lang_code]

    if lang_code.upper() not in LANGUAGE_MAP.values():
        raise ValueError(
            f"ERROR: Invalid Language Code '{lang_code}'! Use codes listed below: {', '.join(LANGUAGE_MAP.values())}")

    translator = deepl.Translator(auth_key)
    translated_text = translator.translate_text(text, target_lang=lang_code.upper())
    return translated_text.text


if __name__ == "__main__":
    try:
        print(translate("Hello, world!", "ZH"))
        print(translate("Hello, world!", "FR"))
        print(translate("Hello, world!", "XYZ"))
    except ValueError as e:
        print(e)