from mockito import when, unstub
import builtins
from io import BytesIO

from sttgoogle import stt

response_json = {'results': [{'alternatives': [{'confidence': 0.9788915, 'transcript': 'how heavy is a cow'}]}], 'totalBilledTime': '15s'}


def test_stt(requests_mock):
    '''
    stt()
    '''
    requests_mock.post(
            'https://speech.googleapis.com/v1/speech:recognize', 
            json=response_json)

    # The content of the file is unimportant if the call to the speech API is mocked.
    when(builtins).open('test_stt_in.wav', 'rb').thenReturn(BytesIO(b"\n\n\n"))

    # auth = subprocess.getoutput('gcloud auth application-default print-access-token')
    auth = "DUMMY"
    speech_sample = 'test_stt_in.wav'
    with open(speech_sample, "rb") as audio_in:
        text = stt(audio_in, auth)
        # returned text must mach the value of transcript in response_json.
        assert text == "how heavy is a cow"
    unstub()
