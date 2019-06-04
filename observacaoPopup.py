import util
import tkinter
from tkinter import *

class ObservacaoPopup:


    def __init__(self, father, directory):

        self.father = father

        exam = util.getExam()

        widthWindowControl = 300
        heightWindowControl = 150
        yControl = int((exam['monitorHeight']/2) - (heightWindowControl/2))
        xControl = int((exam['monitorWidth']/2) - (widthWindowControl/2))

        self.window = Tk()
        self.window.title("Observações")
        self.window.minsize(widthWindowControl, heightWindowControl)
        self.window.geometry('{}x{}+{}+{}'.format(widthWindowControl, heightWindowControl, xControl, yControl))
        self.window.resizable(False, False)
        self.window.config(padx=5, pady=5)

        root = Frame(self.window)
        root.pack(fill="both", expand="True")

        dados = util.getDados(directory)

        tObservacao = Text(root, height=8, width=35)
        tObservacao.grid(row=0, column=0, sticky=W + E, padx=3, pady=3)
        tObservacao.insert(INSERT, dados['observacoes'])
        tObservacao.config(state=DISABLED)

        self.window.protocol("WM_DELETE_WINDOW", self._close)
        self.window.mainloop()

    def _close(self):

        self.father.flagObservacoes = False

        # Fecha a janela
        self.window.destroy()