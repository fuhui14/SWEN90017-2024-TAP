# from .transcribe_with_speaker_resemblyzer import transcribe_with_speaker_resemblyzer
from .transcribe_with_speaker_fasterWhisper import transcribe_with_speaker_fasterWhisper

def transcribe_with_speaker(task_id, audioPath):
    return transcribe_with_speaker_fasterWhisper(task_id, audioPath)
    # return transcribe_with_speaker_resemblyzer(audioPath)