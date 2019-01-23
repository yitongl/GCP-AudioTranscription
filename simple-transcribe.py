from google.cloud import speech_v1p1beta1 as speech
import pandas as pd

client = speech.SpeechClient()
bucket = 'gs://STORAGE_BUCKET_URL/'
audio_file_name = 'press_conference.flac'
speech_file = ( bucket + audio_file_name)

# with open(speech_file, 'rb') as audio_file:
#     content = audio_file.read()

print ('Using Google Speech API to generate transcript .......')

audio = speech.types.RecognitionAudio(uri=speech_file)

config = speech.types.RecognitionConfig(
    encoding=speech.enums.RecognitionConfig.AudioEncoding.LINEAR16,
    language_code='en-US',
    sample_rate_hertz=8000,
    enable_speaker_diarization=True,
    diarization_speaker_count=5,
    enable_word_time_offsets=True,
    enable_automatic_punctuation=True,
    model='phone_call'
    # audio_channel_count=4,
    # enable_separate_recognition_per_channel=True
    )

operation = client.long_running_recognize(config, audio)

print('Waiting for operation to complete...')
response = operation.result(timeout=1200)

# The transcript within each result is separate and sequential per result.
# However, the words list within an alternative includes all the words
# from all the results thus far. Thus, to get all the words with speaker
# tags, you only have to take the words list from the last result:
result = response.results[-1]
# print (response.results)

alternative = result.alternatives[0]

words_dict={"word":[], "start_time":[], "end_time":[], "speaker_tag":[]}

print('Transcript: {}'.format(alternative.transcript))
print('Confidence: {}'.format(alternative.confidence))

# for i, result in enumerate(response.results):
#     alternative = result.alternatives[0]
#     print('-' * 20)
#     print('First alternative of result {}'.format(i))
#     print('Transcript: {}'.format(alternative.transcript))
#     print(alternative.words)

#Printing out the output:
for word_info in alternative.words:
    word = word_info.word
    start_time = word_info.start_time
    end_time = word_info.end_time
    speaker_tag=word_info.speaker_tag
    words_dict["word"].append(word)
    words_dict["start_time"].append(start_time)
    words_dict["end_time"].append(end_time)
    words_dict["speaker_tag"].append(speaker_tag)

words_dict_df=pd.DataFrame(words_dict)
words_dict_df.to_csv('/Users/yitong/downloads/transcription.csv')

                                           