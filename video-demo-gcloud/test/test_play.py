import pytest
from play import play


def test_play_missing_wav():
    '''
    play() must raise FileNotFoundError when the filename given is not the path to a readable file.
    '''
    filename = 'missing.wav'
    # This test MUST raise FileNotFoundError. Not doing so is an error.
    with pytest.raises(FileNotFoundError):
        play(filename)
