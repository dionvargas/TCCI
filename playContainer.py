from emptyContainer import EmptyContainer
import cv2
import tkinter
import util
from tkinter import *


class PlayContainer(EmptyContainer):

    cont = 0
    play = False

    def __init__(self, movie):
        super().__init__()

        self.cap = cv2.VideoCapture(movie)

        width = self.cap.get(3)
        height = self.cap.get(4)

        self.camera = Canvas(self, width=width, height=height)
        self.camera.pack(expand=True)

        controle = Frame(self, height=40)
        controle.pack(side="bottom", fill="x")
        controle.configure(relief="groove", border=3, padx=5, pady=5)

        self.frame_seq = int(self.cap.get(7) - 1)
        self.fps = int(self.cap.get(5))

        self.l_play = StringVar()
        self.l_play.set("Play")
        self.btnPlay = Button(controle, textvariable=self.l_play, command=self._playMovie).pack(side="left", fill="y")
        self.progressBar = Scale(controle, from_=0, to=self.frame_seq, orient=HORIZONTAL, command=self._alteradoScale, showvalue=False)
        self.progressBar.pack(side="left", fill="x", expand=True)
        Button(controle, text=">", command=self._frameAfter).pack(side="right", fill="y")
        Button(controle, text="<", command=self._frameBefore).pack(side="right", fill="y")

        self.showFrame(self.cont)

    def _playMovie(self):
        self.play = not self.play

        if(self.play):
            self.l_play.set("Stop")
            tempo = 1000/self.fps
            self.delay = int(tempo)
            self.exibeVideo()
        else:
            self.l_play.set("Play")

    def _frameBefore(self):
        self.play = False
        self.l_play.set("Play")
        self.cont -= 1
        if self.cont < 0:
            self.cont = 0
        self.progressBar.set(self.cont)
        self.showFrame(self.cont)

    def _frameAfter(self):
        self.play = False
        self.l_play.set("Play")
        self.cont += 1
        if self.cont > self.frame_seq:
            self.cont = self.frame_seq
        self.progressBar.set(self.cont)
        self.showFrame(self.cont)

    def _alteradoScale(self, val):
        self.cont = int(val)
        self.showFrame(val)

    def exibeVideo(self):
        self.cont += 1
        if self.cont > self.frame_seq:
            self.cont = self.frame_seq
            self.play = False
            self.l_play.set("Play")
        self.progressBar.set(self.cont)
        self.showFrame(self.cont)

        if(self.play):
            self.after(self.delay, self.exibeVideo)

    def showFrame(self, valor):
        valor = int(valor)
        if (self.cap.isOpened()):
            self.cap.set(1, valor)
            ret, frame = self.cap.read()
            if ret:
                self.video = util.convertToExibe(frame)
                self.camera.create_image(0, 0, image=self.video, anchor=tkinter.NW)
                self.l_footer.set("Frame " + str(self.cont) + "/" + str(self.frame_seq))

            else:
                self.cap.release()