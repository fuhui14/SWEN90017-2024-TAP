import os
from langdetect import detect
from transformers import MarianMTModel, MarianTokenizer

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_DIR = os.path.join(BASE_DIR, "..", "models")

ALLOWED_TARGET_LANGS = {
    "zh", "fr", "en", "es", "de", "ru", "it", "pt", "nl", "ar", "ja", "ko", "tr", "pl",
    "hi", "th", "vi", "el", "sv", "fi", "id", "da", "no", "cs", "ro", "hu", "sk", "bg",
    "sr", "uk", "he", "ms", "ta", "mr", "bn", "ml", "kn", "te", "gu", "pa", "or", "ne",
    "si", "hr", "sl", "lv", "lt", "et", "eu", "ca", "gl", "cy", "sq", "mk", "is", "af",
    "zu", "xh", "sw", "yo", "am", "km", "lo", "my", "gu", "fil", "sr", "tl"
}


def ensure_model_exists(model_name):
    model_path = os.path.join(MODEL_DIR, model_name)
    if not os.path.exists(model_path):
        print(f"Model {model_name} does not exist. Downloading...")
        tokenizer = MarianTokenizer.from_pretrained(f"Helsinki-NLP/{model_name}")
        model = MarianMTModel.from_pretrained(f"Helsinki-NLP/{model_name}")
        tokenizer.save_pretrained(model_path)
        model.save_pretrained(model_path)
        print(f"Model {model_name} has been downloaded!")
    return model_path


def detect_language(content):
    res = detect(content)
    if res == "zh-cn":
        res = "zh"
    return res


def translate_to_english(content):
    model_name = "opus-mt-mul-en"
    model_path = ensure_model_exists(model_name)

    tokenizer = MarianTokenizer.from_pretrained(model_path)
    model = MarianMTModel.from_pretrained(model_path)

    inputs = tokenizer(content, return_tensors="pt", padding=True, truncation=True)
    translated = model.generate(**inputs)
    return tokenizer.batch_decode(translated, skip_special_tokens=True)[0]


def translate(content, target_lang="zh"):
    if detect_language(content) == target_lang:
        return content

    if target_lang not in ALLOWED_TARGET_LANGS:
        return f"Error: Unsupported target language '{target_lang}', please use a valid Whisper-supported language."

    english_text = translate_to_english(content)
    print(f"Translated to English: {english_text}")

    if target_lang == "en":
        return content

    model_name = f"opus-mt-en-{target_lang}"
    model_path = ensure_model_exists(model_name)

    tokenizer = MarianTokenizer.from_pretrained(model_path)
    model = MarianMTModel.from_pretrained(model_path)

    inputs = tokenizer(english_text, return_tensors="pt", padding=True, truncation=True)
    translated = model.generate(**inputs)
    return tokenizer.batch_decode(translated, skip_special_tokens=True)[0]


if __name__ == "__main__":
    text = "Bonjour, comment ça va ?"
    print(detect_language(text))
    result = translate(text, "zh")
    print(f"Final translation: {result}")
    result = translate(text, "es")
    print(f"Final translation: {result}")
    result = translate(text, "en")
    print(f"Final translation: {result}")
    text = "你好，世界"
    print(detect_language(text))
    result = translate(text, "en")
    print(f"Final translation: {result}")
    result = translate(text, "zh")
    print(f"Final translation: {result}")
    result = translate(text, "es")
    print(f"Final translation: {result}")

    invalid_result = translate(text, "abc")
    print(invalid_result)