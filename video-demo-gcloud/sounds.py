import sqlite3

# Open database file in read-only mode.

con = None
cur = None


def connect():
    global con, cur
    con = sqlite3.connect('file:audio.db?mode=ro', uri=True)
    cur = con.cursor()


def start_sound():
    return cur.execute(
        'SELECT content FROM clips WHERE path=?',
        ('orac on.wav',)).fetchone()[0]


def end_sound():
    return cur.execute(
        'SELECT content FROM clips WHERE path=?',
        ('orac off.wav',)).fetchone()[0]


class ParsePlay():
    def __init__(self, text):
        self.words = text.split()
        if self.words[0] == "play":
            self.do_play = True
            self.parse()
        else:
            self.do_play = False

    def parse(self):
        # Loud or quiet?
        if "loud" in self.words:
            self.volume = "loud"
        elif "quiet" in self.words:
            self.volume = "quiet"
        elif "soft" in self.words:
            self.volume = "quiet"
        else:
            self.volume = None

        # Music of noise?
        if "music" in self.words:
            self.kind = "music"
        elif "noise" in self.words:
            self.kind = "noise"
        elif "sound" in self.words:
            self.kind = "noise"
        else:
            self.kind = None

        # Remove all these words
        ignore_words = {"play", "a", "me", "some", "something", "by", "music", "please", "now", "loud", "quiet", "soft", "noise", "sound"}

        self.search_words = set(self.words).difference(ignore_words)
        return True



