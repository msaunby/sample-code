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

    audio_file = "test_stt_in.wav"
    tts('how heavy is a cow?', audio_file, auth, sample_rate=16000)
 
if __name__ == "__main__":
    main()