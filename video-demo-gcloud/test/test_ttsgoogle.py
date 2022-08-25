from ttsgoogle import tts
from io import BytesIO



response_json = {'audioContent':'ZZZZ'}

def test_tts(requests_mock):
    '''
    tts()
    '''

    requests_mock.post(
            'https://texttospeech.googleapis.com/v1/text:synthesize',
            json=response_json)

    # auth = subprocess.getoutput('gcloud auth application-default print-access-token')
    auth = "DUMMY"
    in_text = "My name is Werner Branes"
    tts(in_text, 'dummy_file.wav', auth)
    assert True
