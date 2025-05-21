import os
import re
from langdetect import detect
from transformers import MarianMTModel, MarianTokenizer
from nltk.tokenize import sent_tokenize
from concurrent.futures import ThreadPoolExecutor, as_completed

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_DIR = os.path.join(BASE_DIR, "..", "models")

LANG_SPEAKER_MAP = {
    "en": "Speaker",
    "zh": "发言者",
    "fr": "Intervenant",
    "es": "Orador"
}

ALLOWED_TARGET_LANGS = {"zh", "en", "fr", "es"}

LANG_MAP = {
    "english": "en",
    "mandarin": "zh",
    "french": "fr",
    "spanish": "es",
    "chinese": "zh"
}

def ensure_model_exists(model_name):
    model_path = os.path.join(MODEL_DIR, model_name)
    if not os.path.exists(model_path):
        print(f"Downloading model: {model_name}")
        tokenizer = MarianTokenizer.from_pretrained(f"Helsinki-NLP/{model_name}")
        model = MarianMTModel.from_pretrained(f"Helsinki-NLP/{model_name}")
        tokenizer.save_pretrained(model_path)
        model.save_pretrained(model_path)
    return model_path


def detect_language(text):
    lang = detect(text)
    return "zh" if lang.startswith("zh") else lang


def translate_sentence_list(sentences, tokenizer, model, target_lan="en", max_workers=8):
    def translate_single(sentence):
        if sentence.strip() == "":
            return ""
        detect_lang = detect_language(sentence)
        if detect_lang == target_lan:
            return sentence
        inputs = tokenizer(sentence, return_tensors="pt", padding=True, truncation=True)
        translated = model.generate(**inputs)
        return tokenizer.batch_decode(translated, skip_special_tokens=True)[0]

    results = [None] * len(sentences)

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_to_index = {
            executor.submit(translate_single, sentence): idx
            for idx, sentence in enumerate(sentences)
        }

        for future in as_completed(future_to_index):
            idx = future_to_index[future]
            try:
                results[idx] = future.result()
            except Exception as e:
                results[idx] = f"[Error translating sentence: {e}]"

    return " ".join(results)


def split_dialogue_blocks(content):
    pattern = r"((Speaker|发言者|Intervenant|Orador)\s+\d+:)"
    parts = re.split(pattern, content)
    blocks = []
    for i in range(1, len(parts), 3):
        speaker = parts[i].strip()  # e.g. Speaker 1:
        utterance = parts[i + 2].strip()
        blocks.append((speaker, utterance))
    return blocks


def translate(content, target_lang="zh"):
    if target_lang.lower() in LANG_MAP.keys():
        target_lang = LANG_MAP.get(target_lang.lower())

    if target_lang not in ALLOWED_TARGET_LANGS:
        return f"Error: Unsupported target language '{target_lang}'"

    blocks = split_dialogue_blocks(content)

    to_english_model = "opus-mt-mul-en"
    to_english_path = ensure_model_exists(to_english_model)
    to_en_tokenizer = MarianTokenizer.from_pretrained(to_english_path)
    to_en_model = MarianMTModel.from_pretrained(to_english_path)

    if target_lang != "en":
        to_target_model = f"opus-mt-en-{target_lang}"
        to_target_path = ensure_model_exists(to_target_model)
        to_target_tokenizer = MarianTokenizer.from_pretrained(to_target_path)
        to_target_model = MarianMTModel.from_pretrained(to_target_path)

    translated_blocks = []
    for speaker, speech in blocks:
        speaker_number = re.findall(r"\d+", speaker)
        speaker_translated = f"{LANG_SPEAKER_MAP.get(target_lang, 'Speaker')} {speaker_number[0]}" if speaker_number else speaker

        sentences = sent_tokenize(speech)

        english_text = translate_sentence_list(sentences, to_en_tokenizer, to_en_model, "en")

        if target_lang == "en":
            final_text = english_text
        else:
            sentences_en = sent_tokenize(english_text)
            final_text = translate_sentence_list(sentences_en, to_target_tokenizer, to_target_model, target_lang)

        translated_blocks.append(f"{speaker_translated}: {final_text.strip()}\n")

    return "\n".join(translated_blocks)


def test_translate():
    french_dialogue = """
    Intervenant 1: Bonjour tout le monde, commençons la réunion.
    Intervenant 2: Oui, nous avons finalisé la conception hier et l’avons partagée avec l’équipe backend. Nous avons également mis à jour le prototype dans Figma en fonction des derniers retours. Le processus a été bien accueilli par l'équipe, et nous avons reçu des commentaires positifs sur l'interface utilisateur. Maintenant, nous devons nous concentrer sur l'intégration avec la base de données et finaliser la connexion à l'API.
    """
    print("Testing French to Chinese translation...")
    result = translate(french_dialogue, target_lang="zh")
    print(result)

    spanish_dialogue = """
    Orador 1: Hola, bienvenidos a la reunión. Hoy vamos a revisar los avances y los próximos pasos en el proyecto.
    Orador 2: Hemos actualizado la propuesta y la hemos enviado al equipo de desarrollo. Estamos esperando su retroalimentación y preparándonos para la próxima fase del proyecto, que incluirá pruebas de integración y la implementación de nuevas características.
    """
    print("\nTesting Spanish to English translation...")
    result = translate(spanish_dialogue, target_lang="en")
    print(result)

    chinese_dialogue = """
    发言者 1: 大家好，欢迎参加今天的会议。今天我们将讨论项目的进展情况以及下一步的计划。首先，我们需要回顾一下上次会议的讨论内容并检查是否有任何待解决的问题。
    发言者 2: 我们已经完成了最新的报告，并已提交给团队。报告中包含了所有必要的分析和数据支持，接下来我们需要准备演示文稿并与客户进行讨论。
    """
    print("\nTesting Chinese to English translation...")
    result = translate(chinese_dialogue, target_lang="en")
    print(result)

    english_dialogue = """
    Speaker 1: Hello everyone, welcome to the meeting. Today, we will be discussing the progress of the project and the next steps. First, we need to review the discussion from the last meeting and check if there are any pending issues to resolve.
    Speaker 2: We have finalized the proposal and shared it with the development team. It includes all the necessary analysis and data support. Next, we need to prepare the presentation and discuss it with the client.
    """
    print("\nTesting English to French translation...")
    result = translate(english_dialogue, target_lang="fr")
    print(result)

    long_english_dialogue = """
    Speaker 1: Good morning, everyone. Today we have a lot to cover. First, we need to review the progress of the current project. The development team has completed the initial phase of the design, and now we need to move on to the next steps. In the coming weeks, we are expecting the first round of user testing to start. Once the tests are complete, we will gather feedback and work on making improvements. This will involve multiple iterations as we fine-tune the product to meet user expectations. Additionally, we will be focusing on integration with the backend systems, which is a crucial part of this project. The next phase will also include finalizing the user interface, which has been a point of discussion among the team. There have been some concerns about performance, but we are confident that with the changes we plan to make, we will be able to address these issues effectively. In the meantime, we need to ensure that all team members are aligned on the next steps, and that everyone has the necessary resources to move forward with the next phase. It will be important to stay on schedule and to address any blockers that may arise during development. Once the user testing is complete, we will gather the results and move on to the next stage of the process, which will include integrating all the components and doing final testing before release.
    """
    print("\nTesting English with more than 200 words in a single speaker's speech...")
    result = translate(long_english_dialogue, target_lang="fr")
    print(result)

    long_english_dialogue = """
    发言者 1: 大家早上好，今天我们有很多内容需要讨论。首先，我们需要回顾当前项目的进展。开发团队已经完成了设计的初步阶段，现在我们需要进入下一步。在接下来的几周里，我们预计第一轮用户测试将开始。测试完成后，我们将收集反馈并进行改进。这将涉及多个迭代过程，我们将不断调整产品，以满足用户的期望。此外，我们还将重点关注与后台系统的集成，这是这个项目的关键部分。下一阶段还将包括最终确定用户界面，这也是团队讨论的一个重点。关于性能方面有一些顾虑，但我们相信通过计划的更改，我们将能够有效地解决这些问题。在此期间，我们需要确保所有团队成员在下一步工作中保持一致，并且每个人都拥有必要的资源来推进下一阶段的工作。按计划推进并解决开发过程中可能出现的任何阻碍非常重要。一旦用户测试完成，我们将收集结果并进入下一阶段，包括集成所有组件并进行发布前的最终测试。
    """
    print("\nTesting Chinese with more than 200 words in a single speaker's speech...")
    result = translate(long_english_dialogue, target_lang="fr")
    print(result)

    mixed_language_dialogue = """
    Speaker 1: Hello everyone, welcome to the meeting. We have a lot of things to discuss today.
    Orador 1: Hola, bienvenidos a todos. Hoy vamos a revisar los avances y los próximos pasos en el proyecto.
    Speaker 2: We need to ensure that everything is on track before the deadline.
    """
    print("\nTesting mixed languages (English + Spanish)...")
    result = translate(mixed_language_dialogue, target_lang="zh")
    print(result)

    mixed_language_dialogue_fr = """
    Speaker 1: Hello everyone, welcome to the meeting. Today we will be discussing the project.
    Intervenant 1: Bonjour à tous, bienvenue à la réunion. Aujourd'hui, nous allons discuter du projet et des prochaines étapes.
    Speaker 2: We have completed the initial design phase, and now we are moving on to the development stage.
    """
    print("\nTesting mixed languages (English + French)...")
    result = translate(mixed_language_dialogue_fr, target_lang="es")
    print(result)

    mixed_language_dialogue_zh = """
    Speaker 1: Hello everyone, welcome to the meeting. Today we will discuss our next steps.
    发言者 1: 大家好，欢迎参加会议。今天我们将讨论下一步的计划。
    Speaker 2: We need to review the progress of the current project and address any outstanding issues.
    """
    print("\nTesting mixed languages (English + Chinese)...")
    result = translate(mixed_language_dialogue_zh, target_lang="fr")
    print(result)

    real_data_test_1 = """
    Speaker 0: Hi Diego, what do you think about the latest politics in Chile?
    
    Speaker 1: Oh well to be honest we are coming presidential elections soon so it's been fun to see like from
    
    Speaker 0: from a distance and will the left of centre candidates.
    
    Speaker 1: Get in again? I'm not sure because there are like three of them now. They're still not sure which of them is going to go.
    
    Speaker 0: So they can like it up. What's it called? Okay.
    """
    print("\nTesting Swinburne University of Technology - Hawthorn Campus 1")
    result = translate(real_data_test_1, target_lang="zh")
    print(result)

    real_data_test_2 = """
    Speaker 0: So I can't like so
    
    Speaker 1: Now you've got a thumb on your web app.
    
    Speaker 0: buttons made from you. How is it? You can watch up, from the right.
    
    Speaker 1: for this weekend I'm traveling to
    
    Speaker 0: I might go to Perth Prolete to what is it?
    
    Speaker 1: called a Rothwell, Rothpress, Rothness Rothwell style.
    
    Speaker 0: Ruf knowonder
    
    Speaker 1: via Quokas.
    """
    print("\nTesting Swinburne University of Technology - Hawthorn Campus 2")
    result = translate(real_data_test_2, target_lang="zh")
    print(result)

    real_data_test_3 = """
    Speaker 1: Hi, so how was the meeting you just at?

    Speaker 0: Fantastic! I met a former student I taught him yesterday.

    Speaker 1: ago was lovely. Oh that's great.

    Speaker 0: So what are they doing now? They are freelancing, they're working as designers and but they will dig out

    Speaker 1: they are there for more projects.
    """
    print("\nTesting Swinburne University of Technology - Hawthorn Campus 3")
    result = translate(real_data_test_3, target_lang="zh")
    print(result)

if __name__ == "__main__":
    test_translate()
