# Research Report: Speaker identifier library

### Any future progress in this research will be updated in this document

# Research List

|    Library     |                                    Version                                    | Basic Learning | Code Implement | Test | Optimization |
| :------------: | :---------------------------------------------------------------------------: | :------------: | :------------: | :--: | :----------: |
|  Resemblyzer   |               [git](https://github.com/resemble-ai/Resemblyzer)               |       x        |       X        |  X   |              |
| pyannote.audio | [version3.3.1](https://github.com/pyannote/pyannote-audio/releases/tag/3.3.1) |       x        |                |      |              |
|  speechbrain   |    [v1.0](https://github.com/speechbrain/speechbrain/releases/tag/v1.0.0)     |       x        |                |      |              |

# Purpose of the Research

In this TAP project, we need to use openAI Whisper for transcription processing, and we also need to provide the function of identifying different speakers. Therefore, we need to use a third-party open source library for local deployment to implement the recognition function.

# Library Info

## pyannote.audio [version3.3.1](https://github.com/pyannote/pyannote-audio/releases/tag/3.3.1)

pyannote.audio is an open-source toolkit written in Python for speaker diarization. Based on PyTorch machine learning framework, it comes with state-of-the-art pretrained models and pipelines, that can be further finetuned to your own data for even better performance.

## speechbrain [v1.0](https://github.com/speechbrain/speechbrain/releases/tag/v1.0.0)

SpeechBrain is an open-source PyTorch toolkit that accelerates Conversational AI development, i.e., the technology behind speech assistants, chatbots, and large language models.

It is crafted for fast and easy creation of advanced technologies for Speech and Text Processing.

## Resemblyzer [git](https://github.com/resemble-ai/Resemblyzer)

Resemblyzer allows you to derive a high-level representation of a voice through a deep learning model (referred to as the voice encoder). Given an audio file of speech, it creates a summary vector of 256 values (an embedding, often shortened to "embed" in this repo) that summarizes the characteristics of the voice spoken.

# Experiment & Result

## Pre-trained Model

Unlike openAI Whisper, pyannote.audio and speechbrain doesn't provide pre-trained model. But we can download the trained model from [Hugging Face](https://huggingface.co/).

However, the Resemblyzer has the pre-trained model base on GE2E(Generalized End to End Loss) model. It is a deep learning method for converting speech into embedding vectors so that the speech embeddings of the same person are close to each other, while the speech embeddings of different people are far away from each other. This allows for efficient speaker verification and recognition.

## Introduction of Hugging face

Hugging Face is an artificial intelligence company focusing on natural language processing (NLP) technology, founded in 2016. It is well-known for its open source Transformers library, which provides developers with a large number of pre-trained models and tools for performing various NLP tasks such as text classification, machine translation, question answering systems, text generation, etc.

## Use of Resemblyzer

Since Resemblyzer provides pre-trained models and is relatively easy to use, I tried using Resemblyzer first.

The code for trying out Resemblyzer can be viewed on git branch "/feature/backend/whisper"

The use of Resemblyzer is as follows：

- Use pydub to split audio into chunks base on the silence detection
- Use resemblyzer to generate the embeddings
- Use DBSCAN to cluster the embeddings and generate labels, the DBSCAN need a threshold to clarify different speaker.

However, there are some optimization we can add:

- We can first transfer all the audio file into ".wav" or ".m4a", these are the acceptable file type for resemblyzer.
- Since we are using the silence detection to split chunks, we can reduce the influence of background noise at first.
  There are several ways to achieve:
  1. Simply add a threshold to the original audio file to filter out audio with a lower decibel level, but the effect is poor and its effect on different environments is uncertain.
  2. Use some library like Noiserreduce, librosa, RNNoise to reduce the background noise.
- Modify the min_silence_len and silence_thresh in the slit_on_silence(), choose better params.

## Use of pyannote.audio and speechbrain

These two libraries are more difficult to use than Resemblyzer, but they also provide more models to choose from, which can produce better results and provide higher accuracy.

To use these two models, we need to first select the appropriate model on the Hugging Face website and download it locally. Then we can use the locally downloaded model for sound recognition processing.

### Specific usage of pyannote.audio and speechbrain experiments are still in progress.

# Conclusion

For now, the main part of the code experiment of Resemblyzer has been completed, and it can be further tested and optimized to achieve better results. The code implementation of pyannote.audio and speechbrain is still in progress and it takes time to select the appropriate pre-trained model for deployment. In general, using Resemblyzer for speaker recognition is a very simple and fast choice, which can be implemented quickly, but the effect will be relatively ordinary. Using pyannote.audio and speechbrain can bring higher accuracy but may require more development time and have higher requirements on the GPU.

# Research Update Record:

- 2024/09/11 Complete code implement and test for Resemblyzer. Complete basic learning for pyannote.audio, speech brain and Resemblyzer. Create research document.
