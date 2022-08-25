#
# G-Cloud credentials are required
# If the G-Cloud SDK is installed the following will work.
#
# export GOOGLE_APPLICATION_CREDENTIALS=my-project-credentials.json
#
# This code will call 'gcloud auth application-default print-access-token' to
# get a token.
#

from record import record
from sttgoogle import stt
from ttsgoogle import tts
from querywolfram import answer_query
from play import play
import sounds
import subprocess
import os
import tkinter
from tkinter import ttk
import time
import threading
import queue


def doQuery(myqueue):
    myqueue.put("listen")
    audio_in_file = 'input.wav'
    record(audio_in_file)
    myqueue.put("answer")
    with open(audio_in_file, "rb") as audio_in:
        text = stt(audio_in, auth)
        os.remove(audio_in_file)
        print("extracted text:", text)
    answer = answer_query(text)
    print(answer)
    audio_out_file = 'output.wav'
    tts(answer, audio_out_file, auth)
    myqueue.put("done")
    play(audio_out_file)
    os.remove(audio_out_file)


def doStartup(myqueue):
    myqueue.put("startup")
    sounds.connect()
    audiodata = sounds.start_sound()
    play(audiodata)


class GuiPart:

    def change_colour(self):
        cidx = self.colour_code
        rgb = [10, 10, 10]
        self.mainframe.after(50, self.change_colour)
        s = ttk.Style(self.master)
        incr = (255 - 100) // 40
        for i in range(40):
            rgb[cidx] = 100 + (((i + self.colour_incr) % 40) * incr)
            s.configure(
                f'x{i}.TLabel',
                background=f'#{rgb[0]:02x}{rgb[1]:02x}{rgb[2]:02x}')

        self.colour_incr -= 1
        self.colour_incr %= 40

    def __init__(self, master, queue, onoffCommand):
        self.queue = queue
        # Set up the GUI

        self.master = master
        self.mainframe = ttk.Frame(master, padding="3 3 12 12")
        self.colour_incr = -1
        self.colour_code = 0
        self.mainframe.grid(
            column=0,
            row=0,
            sticky=(
                tkinter.N,
                tkinter.W,
                tkinter.E,
                tkinter.S))
        master.columnconfigure(0, weight=1)
        master.rowconfigure(0, weight=1)

        mainframe = self.mainframe
        self.onoff_text = tkinter.StringVar()
        self.onoff_text.set('On')
        onoff = ttk.Button(
            mainframe,
            textvariable=self.onoff_text,
            command=onoffCommand)

        onoff.grid(
            column=1, row=20,
            columnspan=10, sticky=tkinter.W)

        ttk.Label(mainframe, text="").grid(column=1, row=1, sticky=tkinter.W)
        ttk.Label(mainframe, text="").grid(column=1, row=2, sticky=tkinter.W)
        ttk.Label(mainframe, text="").grid(column=1, row=3, sticky=tkinter.W)
        ttk.Label(mainframe, text="").grid(column=1, row=4, sticky=tkinter.W)
        ttk.Label(mainframe, text="").grid(column=1, row=5, sticky=tkinter.W)

        for i in range(0, 40):
            ttk.Label(mainframe, text="   ", style=f"x{i}.TLabel").grid(
                column=i, row=6, sticky=tkinter.W)

        ttk.Label(mainframe, text="").grid(column=1, row=7, sticky=tkinter.W)
        ttk.Label(mainframe, text="").grid(column=1, row=8, sticky=tkinter.W)
        ttk.Label(mainframe, text="").grid(column=1, row=9, sticky=tkinter.W)
        ttk.Label(mainframe, text="").grid(column=1, row=10, sticky=tkinter.W)
        ttk.Label(mainframe, text="").grid(column=1, row=11, sticky=tkinter.W)

        for child in mainframe.winfo_children():
            child.grid_configure(padx=1, pady=1)

    def process_incoming(self):
        """Handle all messages currently in the queue, if any."""
        while self.queue.qsize():
            try:
                msg = self.queue.get(0)
                # Check contents of message and do whatever is needed. As a
                # simple test, print it (in real life, you would
                # suitably update the GUI's display in a richer fashion).
                if msg == "startup":
                    self.colour_code = 0
                    self.change_colour()
                    self.onoff_text.set('Off')
                elif msg == "listen":
                    self.colour_code = 1
                    print("Ok, I'm listening")
                elif msg == "answer":
                    self.colour_code = 2
                elif msg == "done":
                    self.colour_code = 0
                else:
                    self.colour_code = 0
                    print(f"I don't know what to do with {msg}")
            except queue.Empty:
                # just on general principles, although we don't
                # expect this branch to be taken in this case
                pass


class ThreadedClient:
    """
    Launch the main part of the GUI and the worker thread. periodicCall and
    endApplication could reside in the GUI part, but putting them here
    means that you have all the thread controls in a single place.
    """

    def __init__(self, master):
        """
        Start the GUI and the asynchronous threads. We are in the main
        (original) thread of the application, which will later be used by
        the GUI as well. We spawn a new thread for the worker (I/O).
        """
        self.master = master

        # Create the queue
        self.queue = queue.Queue()

        # Set up the GUI part
        self.gui = GuiPart(master, self.queue, self.onoff)

        self.ready = False

        # Set up the thread to do asynchronous I/O
        # More threads can also be created and used, if necessary
        self.running = 1
        self.thread1 = threading.Thread(target=self.worker_thread1)
        self.thread1.start()

        # Start the periodic call in the GUI to check if the queue contains
        # anything
        self.periodic_call()

    def periodic_call(self):
        """
        Check every 200 ms if there is something new in the queue.
        """
        self.gui.process_incoming()
        if not self.running:
            # This is the brutal stop of the system. You may want to do
            # some cleanup before actually shutting it down.
            import sys
            sys.exit(1)
        self.master.after(200, self.periodic_call)

    def worker_thread1(self):
        while self.running:
            time.sleep(0.2)
            if self.ready:
                doStartup(self.queue)
                print("we are off")
                doQuery(self.queue)

    def onoff(self):
        if not self.ready:
            self.ready = True
        else:
            # play(sounds.end_sound())
            self.running = 0


if __name__ == "__main__":
    # Authentication key needed for Google APIs
    global auth
    auth = subprocess.getoutput(
        'gcloud auth application-default print-access-token')
    #
    print("auth is", auth)
    root = tkinter.Tk()
    root.title("Ekco")
    client = ThreadedClient(root)
    root.mainloop()
