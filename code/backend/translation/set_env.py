import nltk
nltk.download('punkt')
nltk.download('punkt_tab')
from translate import ensure_model_exists

ensure_model_exists("opus-mt-mul-en")
ensure_model_exists("opus-mt-en-zh")
ensure_model_exists("opus-mt-en-fr")
ensure_model_exists("opus-mt-en-es")