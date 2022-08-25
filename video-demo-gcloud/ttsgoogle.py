
#
# Based on curl example at https://cloud.google.com/text-to-speech/docs/quickstart-protocol
#
import requests
import base64

url = 'https://texttospeech.googleapis.com/v1/text:synthesize'


json_data = {
    "input": {
        "text": ""
    },
    "voice": {
        "languageCode": "en-gb",
        "name": "en-GB-Standard-B"
    },
    "audioConfig": {
        "audioEncoding": ""
    }
}


def tts(
        text_in: str,
        filename_out: str,
        auth: str,
        encoding: str = "LINEAR16",
        sample_rate=None) -> bool:
    """
    Allowed encodings: MP3 (.mp3), LINEAR16 (.wav), OGG_OPUS (.ogg)
    """

    headers = {'Authorization': 'Bearer ' + auth,
               'Content-Type': 'application/json; charset=utf-8'}
    json_data['input']['text'] = text_in
    json_data['audioConfig']['audioEncoding'] = encoding
    if sample_rate:
        json_data['audioConfig']['sampleRateHertz'] = sample_rate

    response = requests.post(url, json=json_data, headers=headers)

    if response.ok:
        with open(filename_out, "wb") as out:
            out.write(base64.b64decode(response.json()['audioContent']))
        return True
    else:
        return False
