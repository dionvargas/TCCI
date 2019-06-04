import util
import tkinter
from tkinter import *

class PacientePopup:


    def __init__(self, father, directory):

        self.father = father

        exam = util.getExam()

        widthWindowControl = 300
        heightWindowControl = 150
        yControl = int((exam['monitorHeight']/2) - (heightWindowControl/2))
        xControl = int((exam['monitorWidth']/2) - (widthWindowControl/2))

        self.window = Tk()
        self.window.title("Dados do paciente")
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
            nome = StringVar(root)
            nome.set("Nome: " + dados['nome'])
            Label(root, textvariable=nome).grid(column=0, row=0, sticky=W+N)
            dataNascimento = StringVar(root)
            dataNascimento.set("Data de Nascimento: " + dados['dataNascimento'])
            Label(root, textvariable=dataNascimento).grid(column=0, row=1, sticky=W+N)
            sexo = StringVar(root)
            sexo.set("Sexo: " + dados['sexo'])
            Label(root, textvariable=sexo).grid(column=0, row=2, sticky=W+N)
            estadoCivil = StringVar(root)
            estadoCivil.set("Estado Civil: " + dados['estadoCivil'])
            Label(root, textvariable=estadoCivil).grid(column=0, row=3, sticky=W+N)
            profisao = StringVar(root)
            profisao.set("Profisão: " + dados['profisao'])
            Label(root, textvariable=profisao).grid(column=0, row=4, sticky=W+N)
            telefone = StringVar(root)
            telefone.set("Telefone: " + dados['telefone'])
            Label(root, textvariable=telefone).grid(column=0, row=5, sticky=W+N)

        self.window.protocol("WM_DELETE_WINDOW", self._close)
        self.window.mainloop()

    def _close(self):

        self.father.flagDadosPaciente = False

        # Fecha a janela
        self.window.destroy()