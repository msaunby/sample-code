import pytest
import sounds


def test_start_sound():
    assert True


def test_parse_play():
    p = sounds.ParsePlay("play some loud music by beethoven")
    assert p.words == ["play", "some", "loud", "music", "by", "beethoven"]
    assert p.do_play is True
    assert p.volume == "loud"
    assert p.kind == "music"
    assert p.search_words == {"beethoven"}
