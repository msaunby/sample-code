import pyaudio
import wave
import io
CHUNK = 1024


def play(audio_in: any):
    '''
    audio_in is either a path to a WAV file or bytes containing WAV audio.
    '''
    p = pyaudio.PyAudio()

    if isinstance(audio_in, type(b'')):
        wf = wave.open(io.BytesIO(audio_in), 'rb')
    else:
        wf = wave.open(audio_in, 'rb')

    stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                    channels=wf.getnchannels(), rate=wf.getframerate(),
                    output=True)

    # read data
    data = wf.readframes(CHUNK)

    # play stream
    while len(data) > 0:
        stream.write(data)
        data = wf.readframes(CHUNK)

    # stop stream
    stream.stop_stream()
    stream.close()

    # close PyAudio
    p.terminate()
