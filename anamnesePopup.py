import util
import tkinter
from tkinter import *

class AnamnesePopup:


    def __init__(self, father, directory):

        self.father = father

        exam = util.getExam()

        widthWindowControl = 300
        heightWindowControl = 125
        yControl = int((exam['monitorHeight']/2) - (heightWindowControl/2))
        xControl = int((exam['monitorWidth']/2) - (widthWindowControl/2))

        self.window = Tk()
        self.window.title("Dados da anamnese")
        self.window.minsize(widthWindowControl, heightWindowControl)
        self.window.geometry('{}x{}+{}+{}'.format(widthWindowControl, heightWindowControl, xControl, yControl))
        self.window.resizable(False, False)
        self.window.config(padx=5, pady=5)

        root = Frame(self.window, relief="groove", border=3)
        root.pack(fill="both", expand="True")

        dados = util.getDados(directory)

        if(dados['pacienteAnonimo'] is True):
            Label(root, text="Paciente Anônimo").grid(column=0, row=0)
        else:
            if (dados['problemaSaude'] is "N"):
                Label(root, text="Possui problema de saúde: Não").grid(column=0, row=0, sticky=W + N)
            else:
                psaude = StringVar(root)
                psaude.set("Possui problema de saúde: " + dados['tProblemaSaude'])
                Label(root, textvariable=psaude).grid(column=0, row=0, sticky=W+N)
            if (dados['medicamento'] is "N"):
                Label(root, text="Usa algum medicamento: Não").grid(column=0, row=1, sticky=W + N)
            else:
                medicamento = StringVar(root)
                medicamento.set("Usa algum medicamento: " + dados['tMedicamento'])
                Label(root, textvariable=medicamento).grid(column=0, row=1, sticky=W+N)
            if (dados['tratamento'] is "N"):
                Label(root, text="Está sob algum tratamento médico: Não").grid(column=0, row=2, sticky=W + N)
            else:
                tratamento = StringVar(root)
                tratamento.set("Está sob algum tratamento médico: " + dados['tTratamento'])
                Label(root, textvariable=tratamento).grid(column=0, row=2, sticky=W+N)
            if (dados['alergia'] is "N"):
                Label(root, text="Possui alergia a algum medicamento: Não").grid(column=0, row=3, sticky=W + N)
            else:
                medicamento = StringVar(root)
                medicamento.set("Possui alergia a algum medicamento: " + dados['tAlergia'])
                Label(root, textvariable=medicamento).grid(column=0, row=3, sticky=W+N)
            if (dados['lentes'] is "L"):
                Label(root, text="Usa lentes corretivas: Lentes de contato").grid(column=0, row=4, sticky=W + N)
            elif (dados['lentes'] is "O"):
                Label(root, text="Usa lentes corretivas: Óculos").grid(column=0, row=4, sticky=W + N)
            else:
                Label(root, text="Usa lentes corretivas: Não").grid(column=0, row=4, sticky=W + N)


        self.window.protocol("WM_DELETE_WINDOW", self._close)
        self.window.mainloop()

    def _close(self):

        self.father.flagDadosAnamnese = False

        # Fecha a janela
        self.window.destroy()