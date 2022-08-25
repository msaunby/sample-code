# G-Cloud credentials are required
# If the G-Cloud SDK is installed the following will work.
#
# export GOOGLE_APPLICATION_CREDENTIALS=my-project-credentials.json
#
# This code will call 'gcloud auth application-default print-access-token' to
# get a token.
#
# Based on curl example at https://cloud.google.com/text-to-speech/docs/quickstart-protocol
#
from typing import BinaryIO
import requests
import base64


url = 'https://speech.googleapis.com/v1/speech:recognize'

# https://cloud.google.com/speech-to-text/docs/reference/rest/v1/RecognitionConfig#AudioEncoding


json_data = {
    "config": {
        "encoding": "LINEAR16",
        "sampleRateHertz": 16000,
        "languageCode": "en-US",
        "enableWordTimeOffsets": False
    },
    "audio": {
        "content": ""
    }
}


def stt_raw(audio_in: BinaryIO, auth: str, encoding="LINEAR16") -> str:
    '''
    Expects a FLAC or WAV file. See ... for more information.
    '''

    headers = {'Authorization': 'Bearer ' + auth,
               'Content-Type': 'application/json; charset=utf-8'}

    audio_bytes = audio_in.read()
    json_data["config"]["encoding"] = encoding
    json_data["audio"]["content"] = base64.b64encode(
        audio_bytes).decode('utf-8')
    return requests.post(url, json=json_data, headers=headers)


def stt(audio_in: BinaryIO, auth: str, encoding="LINEAR16") -> str:
    '''
    Expects a FLAC or WAV file. See ... for more information.
    '''
    response = stt_raw(audio_in, auth, encoding)
    if not response.ok:
        print(response, response.json()['error']['message'])
        return ""
    else:
        data = response.json()
        if 'results' in data:
            return data['results'][0]['alternatives'][0]['transcript']
        else:
            return ""
