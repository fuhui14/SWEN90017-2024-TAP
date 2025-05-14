# from .transcribe_with_speaker_resemblyzer import transcribe_with_speaker_resemblyzer
from .transcribe_with_speaker_fasterWhisper import transcribe_with_speaker_fasterWhisper

def transcribe_with_speaker(audioPath):
    return transcribe_with_speaker_fasterWhisper(audioPath)
    # return transcribe_with_speaker_resemblyzer(audioPath)