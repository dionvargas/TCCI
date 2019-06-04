from emptyContainer import EmptyContainer

from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

import os
import cv2
import util
from tkinter import *
from tkinter import messagebox
import numpy as np
from PIL import Image, ImageTk

from pacientePopup import PacientePopup
from anamnesePopup import AnamnesePopup
from observacaoPopup import ObservacaoPopup

class ResultadoContainer(EmptyContainer):

    def __init__(self, father, directory):
        super().__init__()

        self.directory = directory
        self.father = father

        self.pos = []
        self.posX = []
        self.posY = []
        self.numFrame = 1
        self.flagDadosPaciente = False
        self.flagDadosAnamnes = False
        self.flagObservacoes = False

        if(self._validate(self.directory)):

            self.cap = cv2.VideoCapture(directory+"/exame.mp4")

            self.frame_seq = int(self.cap.get(7) - 1)

            procDados = open(directory + "/dados.txt", "r")
            for linha in procDados:
                tmp = linha.split("\t")
                self.pos.append(int(tmp[0]))
                self.posX.append(int(tmp[1]))
                self.posY.append(int(tmp[2]))
            procDados.close()

            root = Frame(self, padx=3, pady=3, width=200)
            root.pack(expand="False", fill="both")

            cabecalho = Frame(self, padx=3, pady=3)
            cabecalho.pack(expand=True, fill="x")

            dados = Frame(cabecalho, padx=3, pady=3, relief="groove", border=3)
            dados.pack(expand=True, fill="both", side=LEFT)

            if os.path.isfile(self.directory + "/dados.json"):

                dados.grid_columnconfigure(0, weight=40)
                dados.grid_columnconfigure(1, weight=40)
                dados.grid_columnconfigure(2, weight=40)
                dados.grid_columnconfigure(3, weight=40)

                dadosExame = util.getDados(directory)
                config = util.getConfig()

                f1 = Frame(dados, padx=3, pady=3)
                f1.grid(column=0, row=0, sticky=W+S+N+E)
                Label(f1, text="Dados de captura:", font='Helvetica 10 bold').grid(column=0, row=0, sticky=W)

                width = StringVar()
                height = StringVar()

                for key in config['resolutions']:
                    if key['resName'] == "Mode " + str(dadosExame['cameraMode']):
                        width.set("Comprimento: " + str(key['width']) + "px")
                        height.set("Altura: " + str(key['height']) + "px")

                Label(f1, textvariable=width).grid(column=0, row=1, sticky=W)

                Label(f1, textvariable=height).grid(column=0, row=2, sticky=W)

                fps = StringVar()
                fps.set("FPS: " + str(dadosExame['fps']))
                Label(f1, textvariable=fps).grid(column=0, row=3, sticky=W)

                data = StringVar()
                data.set("Data: " + dadosExame['data'])
                Label(f1, textvariable=data).grid(column=0, row=4, sticky=W)

                hora = StringVar()
                hora.set("Horário: " + dadosExame['hora'])
                Label(f1, textvariable=hora).grid(column=0, row=5, sticky=W)

                f2 = Frame(dados, padx=3, pady=3)
                f2.grid(column=1, row=0, sticky=W+S+N+E)

                Label(f2, text="Luminosidade:", font='Helvetica 10 bold').grid(column=0, row=0, columnspan=4, sticky=W)
                ledIr = StringVar()
                ledIr.set("IR: " + str(dadosExame['ledIr']))
                Label(f2, textvariable=ledIr).grid(column=0, row=1, sticky=W)

                ledBr = StringVar()
                ledBr.set("BR: " + str(dadosExame['ledBr']))
                Label(f2, textvariable=ledBr).grid(column=0, row=2, sticky=W)

                f3 = Frame(dados, padx=3, pady=3)
                f3.grid(column=2, row=0, sticky=W+S+N+E)

                Label(f3, text="Imagem:", font='Helvetica 10 bold').grid(column=0, row=0, sticky=W)
                contraste = StringVar()
                contraste.set("Contraste: " + str(dadosExame['contraste']))
                Label(f3, textvariable=contraste).grid(column=0, row=1, sticky=W)

                saturacao = StringVar()
                saturacao.set("Saturacao: " + str(dadosExame['saturacao']))
                Label(f3, textvariable=saturacao).grid(column=0, row=2, sticky=W)

                nitidez = StringVar()
                nitidez.set("Nitidez: " + str(dadosExame['nitidez']))
                Label(f3, textvariable=nitidez).grid(column=0, row=3, sticky=W)

                brilho = StringVar()
                brilho.set("Brilho: " + str(dadosExame['brilho']))
                Label(f3, textvariable=brilho).grid(column=0, row=4, sticky=W)

                f4 = Frame(dados, padx=3, pady=3)
                f4.grid(column=3, row=0, sticky=W+S+N+E)

                if(dadosExame['colorEfect'] is False):
                    Label(f4, text="Efeito de cor: Não", font='Helvetica 10 bold').grid(column=0, row=0, sticky=W)
                else:
                    Label(f4, text="Efeito de cor: Sim", font='Helvetica 10 bold').grid(column=0, row=0, sticky=W)

                    rColor = StringVar()
                    rColor.set("R: " + str(dadosExame['rColor']))
                    Label(f4, textvariable=rColor).grid(column=0, row=1, sticky=W)

                    gColor = StringVar()
                    gColor.set("G: " + str(dadosExame['gColor']))
                    Label(f4, textvariable=gColor).grid(column=0, row=2, sticky=W)

                    bColor = StringVar()
                    bColor.set("B: " + str(dadosExame['bColor']))
                    Label(f4, textvariable=bColor).grid(column=0, row=3, sticky=W)
            else:
                Label(dados, text="Não foi possível encontrar o arquivo de dados").grid(column=0, row=0, sticky=W)

            display = Frame(cabecalho, padx=3, pady=3, relief="groove", border=3)
            display.pack(expand=False, fill="both", side=RIGHT)
            self.imgDisplay = Canvas(display, width=173, height=130)
            self.imgDisplay.grid(column=0, row=0, columnspan=3, sticky=W)
            btnBefore = Button(display, text="<", width=5, command=self._frameBefore)
            btnBefore.grid(column=0, row=1, sticky=W)
            self.time = StringVar()
            self.time.set(self.numFrame)
            eTempo = Entry(display, textvariable=self.time, width=4)
            eTempo.bind("<Return>", self._setTempo)
            eTempo.grid(column=1, row=1, sticky=E+W)
            btnAfter = Button(display, text=">", width=5, command=self._frameAfter)
            btnAfter.grid(column=2, row=1, sticky=E)

            botoes = Frame(cabecalho, padx=3, pady=3, relief="groove", border=3)
            botoes.pack(expand=False, fill="both", side=RIGHT)
            btnPaciente = Button(botoes, text="Paciente", width=10, command=lambda: self._dadosPaciente(self.directory))
            btnPaciente.grid(column=0, row=0, sticky=W)
            btnAnamnese = Button(botoes, text="Anamnese", width=10, command=lambda: self._dadosAnamnese(self.directory))
            btnAnamnese.grid(column=0, row=1, sticky=W)
            btnObservacoes = Button(botoes, text="Observações", width=10, command=lambda: self._observacoes(self.directory))
            btnObservacoes.grid(column=0, row=2, sticky=W)
            btnExportar = Button(botoes, text="Exportar", width=10, command=lambda: self._exportar())
            btnExportar.grid(column=0, row=3, sticky=W)

            self.v_posX = StringVar()
            self.v_posX.set("X = " + str(self.posX[self.numFrame]))
            lPosX = Label(botoes, textvariable=self.v_posX)
            lPosX.grid(column=0, row=4, sticky=W)
            self.v_posY = StringVar()
            self.v_posY.set("Y = " + str(self.posY[self.numFrame]))
            lPosY = Label(botoes, textvariable=self.v_posY)
            lPosY.grid(column=0, row=5, sticky=W)

            # --------------- GRÁFICO DE X -------------------
            chartX = Figure(figsize=(10, 2), facecolor='white')

            self.xAxis = chartX.add_subplot(111)  # 1 row, 1 column
            self.xTValues = self.pos
            self.xValues = self.posX
            self.xTimeBar = [np.min(self.posX), np.max(self.posX)]
            self.xAxis.plot(self.xTValues, self.xValues)
            self.xAxis.plot([self.numFrame, self.numFrame], self.xTimeBar)

            self.xAxis.set_ylabel('Posição X')
            self.xAxis.set_xlabel('Tempo')
            self.xAxis.grid()

            self.canvasX = FigureCanvasTkAgg(chartX, master=self)
            self.canvasX._tkcanvas.pack()

            # --------------- GRÁFICO DE Y -------------------
            chartY = Figure(figsize=(10, 2), facecolor='white')
            self.yAxis = chartY.add_subplot(111)  # 1 row, 1 column
            self.yTValues = self.pos
            self.yValues = self.posY
            self.yTimeBar = [np.min(self.posY), np.max(self.posY)]
            self.yAxis.plot(self.yTValues, self.yValues)
            self.yAxis.plot([self.numFrame, self.numFrame], self.yTimeBar)

            self.yAxis.set_ylabel('Posição Y')
            self.yAxis.set_xlabel('Tempo')
            self.yAxis.grid()

            self.canvasY = FigureCanvasTkAgg(chartY, master=self)
            self.canvasY._tkcanvas.pack()

            self.showFrame(self.numFrame)

        else:
            image = Image.open("resources/horus.png")
            image = image.resize((580, 168), Image.ANTIALIAS)
            imagem = ImageTk.PhotoImage(image)
            w = Label(self, image=imagem)
            w.imagem = imagem
            w.pack(expand=True)

    def _validate(self, directory):
        if not os.path.isfile(directory+"/exame.mp4"):
            t = messagebox.showerror("Erro", "Não foi possível encontrar o arquivo de vídeo")
            return False

        elif not os.path.isfile(directory + "/dados.txt"):
            messagebox.showerror("Erro", "Não foi possível encontrar o arquivo de processamento")
            return False

        return True

    def _frameBefore(self):
        self.numFrame -= 1
        if self.numFrame < 0:
            self.numFrame = 0
        self.changeFrame(self.numFrame)

    def _frameAfter(self):
        self.numFrame += 1
        if self.numFrame > self.frame_seq:
            self.numFrame = self.frame_seq
        self.changeFrame(self.numFrame)

    def _setTempo(self, event):
        frame = event.widget.get()
        if(util.validateInt(frame)):
            frame = int(frame)
            if(frame > 1 and frame < np.max(self.yTValues)):
                self.numFrame = frame
        self.changeFrame(self.numFrame)


    def changeFrame(self, numFrame):
        self.showFrame(numFrame)
        self.time.set(numFrame)
        self.v_posX.set("X = " + str(self.posX[numFrame]))
        self.v_posY.set("Y = " + str(self.posY[numFrame]))
        self.replot()

    def showFrame(self, valor):
        valor = int(valor)
        if (self.cap.isOpened()):
            self.cap.set(1, valor)
            ret, frame = self.cap.read()
            x, y, frame = util.findPupila(frame, 3)
            if ret:
                self.video = util.convertToExibe(frame, 173, 130)
                self.imgDisplay.create_image(0, 0, image=self.video, anchor=NW)
            else:
                self.cap.release()

    def replot(self):

        # Gráfico X
        self.xAxis.cla()
        self.xAxis.grid()
        self.xAxis.plot(self.xTValues, self.xValues)
        self.xAxis.plot([self.numFrame, self.numFrame], self.xTimeBar)
        self.xAxis.set_ylabel('Posição X')
        self.xAxis.set_xlabel('Tempo')
        self.canvasX.draw()

        # Gráfico Y
        self.yAxis.cla()
        self.yAxis.grid()
        self.yAxis.plot(self.yTValues, self.yValues)
        self.yAxis.plot([self.numFrame, self.numFrame], self.yTimeBar)
        self.yAxis.set_ylabel('Posição Y')
        self.yAxis.set_xlabel('Tempo')
        self.canvasY.draw()

    def _dadosPaciente(self, directory):
        if(not self.flagDadosPaciente):
            self.flagDadosPaciente = True
            PacientePopup(self, directory)

    def _dadosAnamnese(self, directory):
        if (not self.flagDadosAnamnes):
            self.flagDadosAnamnes = True
            AnamnesePopup(self, directory)

    def _observacoes(self, directory):
        if (not self.flagObservacoes):
            self.flagObservacoes = True
            ObservacaoPopup(self, directory)

    def _exportar(self):
        messagebox.showinfo("Informação", "A ser implementado no TCC II")
