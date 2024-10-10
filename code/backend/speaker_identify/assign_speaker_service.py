import numpy as np
from code.backend.speaker_identify.identify_service import speaker_identifier


def assign_speakers_to_transcription(result):
    if result is None:
        return None
    
    # Get the speaker segments
    segments = result['segments']

    # Get the speaker labels and chunk times using the speaker_identifier function
    labels, chunk_times = speaker_identifier('temp_audio')

    # Process the speaker segments and associate them with the speaker labels
    transcriptions = []
    for segment in segments:
        start = segment['start'] * 1000  # convert to milliseconds
        end = segment['end'] * 1000
        text = segment['text']
        print(segment['start'], segment['end'], text)

        # find the speaker label for the segment
        speaker_label = None
        for i, (chunk_start, chunk_end) in enumerate(chunk_times):
            if (chunk_start <= end) and (chunk_end >= start):
                speaker_label = labels[i]
                break
        
        # Add the transcription to the list
        transcriptions.append({
            'speaker': speaker_label if speaker_label is not None else 'Unknown',
            'text': text.strip(),
            'start': start / 1000,  # convert back to seconds
            'end': end / 1000
        })

    # speaker_identifier('temp_audio')
    print(transcriptions)

    # convert np.int64 to int
    for entry in transcriptions:
        if isinstance(entry["speaker"], np.int64):
            entry["speaker"] = int(entry["speaker"])


    # merge the speaker segments with same speaker identifies
    merged_data = []
    current_segment = transcriptions[0]

    for i in range(1, len(transcriptions)):
        next_segment = transcriptions[i]
        
        # if the speaker is the same, merge the segments
        if current_segment['speaker'] == next_segment['speaker']:
            current_segment['text'] += ' ' + next_segment['text']
            current_segment['end'] = next_segment['end']
        else:
            # if the speaker is different, add the current segment to the merged data and start a new segment
            merged_data.append(current_segment)
            current_segment = next_segment
    
    # add the last segment to the merged data
    merged_data.append(current_segment)

    return merged_data