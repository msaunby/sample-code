from record import record


def test_record():
    filename = 'test.wav'
    result = record(filename, 0.1)
    assert result
