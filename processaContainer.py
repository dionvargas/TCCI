from emptyContainer import EmptyContainer
import cv2
import tkinter
import util
import os
from tkinter import *
from tkinter import messagebox


class ProcessaContainer(EmptyContainer):

    cont = 1

    def __init__(self, father, movie):
        super().__init__()

        global posX, posY, pos
        posX = []
        posY = []
        pos = []

        self.movie = movie
        self.concluido = False
        self.processando = False
        self.cancelado = False
        self.father = father

        self.cap = cv2.VideoCapture(self.movie)

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
        self.l_play.set("Iniciar")
        self.btnPlay = Button(controle, textvariable=self.l_play, command=self._processMovie).pack(side="right", fill="y")
        self.progressBar = Scale(controle, from_=0, to=self.frame_seq, orient=HORIZONTAL, state=DISABLED, showvalue=False)
        self.progressBar.pack(side="left", fill="x", expand=True)

        self.showFrame(self.cont)

    def _processMovie(self):
        global pos, posX, posY
        if self.concluido == True:
            self.father._resultado(self.directory)
        else:
            if(self.processando == True):
                self.l_play.set("Reiniciar")
                self.processando = False
                self.cont = 1
                pos = []
                posX = []
                posY = []

            else:
                self.directory = self.movie
                position = len(self.directory) - 1
                while position >= 0:
                    # No linux mudar a barra para o outro lado
                    if (self.directory[position] is '/'):
                        break
                    else:
                        self.directory = self.directory[:-1]
                    position -= 1

                if os.path.isfile(self.directory + "dados.txt"):
                    result = messagebox.askquestion("Erro", "O arquivo já foi processado. Deseja processar novamente?")
                    if result == 'yes':
                        os.remove(self.directory + "dados.txt")
                        self.processando = True
                        self.l_play.set("Cancelar")
                        tempo = 1000 / self.fps
                        self.delay = int(tempo)
                        self.exibeVideo()
                else:
                    self.processando = True
                    self.l_play.set("Cancelar")
                    tempo = 1000 / self.fps
                    self.delay = int(tempo)
                    self.exibeVideo()

    def exibeVideo(self):
        global posX, posY, ang
        if self.cont > self.frame_seq:
            self.cont = self.frame_seq
            self.processando = False
            self.l_play.set("Concluído")
            self.concluido = True
            print(pos)
            print(posX)
            print(posY)

            arq = open(self.directory+"dados.txt", "w")
            for i in range(self.frame_seq):
                arq.write(str(pos[i]))
                arq.write("\t")
                arq.write(str(posX[i]))
                arq.write("\t")
                arq.write(str(posY[i]))
                arq.write("\n")
            arq.close()

        self.progressBar.config(state=NORMAL)
        self.progressBar.set(self.cont)
        self.progressBar.config(state=DISABLED)
        self.showFrame(self.cont)
        self.cont += 1
        if(self.processando):
            self.after(self.delay, self.exibeVideo)

    def showFrame(self, valor):
        global posX, posY, pos

        valor = int(valor)
        if (self.cap.isOpened()):
            self.cap.set(1, valor)
            ret, frame = self.cap.read()
            x, y, frame = util.findPupila(frame)
            posX.append(x)
            posY.append(y)
            pos.append(valor)
            if ret:
                self.video = util.convertToExibe(frame)
                self.camera.create_image(0, 0, image=self.video, anchor=tkinter.NW)
                self.l_footer.set("Frame " + str(self.cont) + "/" + str(self.frame_seq))

            else:
                self.cap.release()