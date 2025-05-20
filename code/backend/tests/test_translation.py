# import pytest
# from unittest.mock import patch, MagicMock
# from translation.translate import translate, split_dialogue_blocks
#
#
# def test_split_dialogue_blocks_basic():
#     content = "Speaker 1: Hello.\nSpeaker 2: How are you?"
#     blocks = split_dialogue_blocks(content)
#     assert len(blocks) == 2
#     assert blocks[0] == ("Speaker 1:", "Hello.")
#     assert blocks[1] == ("Speaker 2:", "How are you?")
#
#
# @patch("translation.translate.MarianTokenizer.from_pretrained")
# @patch("translation.translate.MarianMTModel.from_pretrained")
# @patch("translation.translate.translate_sentence_list", return_value="这是翻译结果")
# def test_translate_en_to_zh(mock_translate, mock_model, mock_tokenizer):
#     mock_tokenizer.return_value = MagicMock()
#     mock_model.return_value = MagicMock()
#
#     result = translate("Speaker 1: Hello. How are you?", target_lang="zh")
#
#     assert "发言者 1" in result
#     assert "这是翻译结果" in result
#
#
# @patch("translation.translate.MarianTokenizer.from_pretrained")
# @patch("translation.translate.MarianMTModel.from_pretrained")
# @patch("translation.translate.translate_sentence_list", return_value="")
# def test_translate_handles_empty_content(mock_translate, mock_model, mock_tokenizer):
#     mock_tokenizer.return_value = MagicMock()
#     mock_model.return_value = MagicMock()
#
#     input_text = "Speaker 1:    \nSpeaker 2: "
#     result = translate(input_text, target_lang="en")
#
#     assert "Speaker 1" in result
#     assert "Speaker 2" in result
#
