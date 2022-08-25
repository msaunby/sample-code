# G-Cloud credentials are required
# If the G-Cloud SDK is installed the following will work.
#
# export GOOGLE_APPLICATION_CREDENTIALS=my-project-credentials.json
#
# This code will call 'gcloud auth application-default print-access-token' to
# get a token.

from record import record

from sttgoogle import stt

from ttsgoogle import tts

from querywolfram import answer_query

from play import play

import subprocess

import os


def main():
    auth = subprocess.getoutput(
        'gcloud auth application-default print-access-token')

    # Rather than record from the mic we use TTS to create an audio file
    # with the question.
    # Note that the encoding must be set as the default MP3 audio is not
    # acceptable as STT input.

    text = "1 2 3 4"

    if False:
        audio_file = "input.ogg"
        tts('how heavy is a cow?', audio_file, auth,
            encoding="OGG_OPUS", sample_rate=16000)
        with open(audio_file, "rb") as audio_in:
            text = stt(audio_in, auth, encoding="OGG_OPUS")
        print(text)

    else:
        audio_in_file = 'input.wav'
        record(audio_in_file)
        with open(audio_in_file, "rb") as audio_in:
            text = stt(audio_in, auth)
            os.remove(audio_in_file)
        print(text)

    answer = answer_query(text)
    print(answer)

    audio_out_file = 'output.wav'
    tts(answer, audio_out_file, auth)
    play(audio_out_file)
    os.remove(audio_out_file)

if __name__ == "__main__":
    main()