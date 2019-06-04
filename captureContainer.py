import os
import tkinter
import subprocess
import platform
import util
import RPi.GPIO as gpio
import picamera

from tkinter import ttk
from datetime import datetime
from previewConfig import PreviewConfig
from emptyContainer import EmptyContainer

from tkinter import *
from tkinter import messagebox

global exam
global config

class CaptureContainer(EmptyContainer):

    def __init__(self):
        super().__init__()

        exam = util.getExam()
        config = util.getConfig()

        self.l_footer.set("Modo de captura")

        # __________________________________________________________________________________________________________
        # Frame Raiz
        root = Frame(self, padx=3, pady=3)
        root.pack(expand="True", fill="both")
        
        # __________________________________________________________________________________________________________
        # Frame Dados
        dados = Frame(root, border=1, relief="raised")
        dados.pack(expand="True", fill="both")
        
        dadosPaciente = Frame(dados, border=1, relief="groove")
        dadosPaciente.grid(row=0, column=0, sticky="W", padx=3, pady=3)
        Label(dadosPaciente, text="Dados do paciente", font='bold').grid(row=0, column=0, sticky=W, padx=3, pady=3)

        self.pacienteAnonimo = BooleanVar()
        self.pacienteAnonimo.set(False)
        self.checkAnonimo = Checkbutton(dadosPaciente, text="Paciente anônimo", var=self.pacienteAnonimo, offvalue=False, onvalue=True, command=self._checkAnonimo)
        self.checkAnonimo.grid(column=6, row=0, sticky=E)

        # Dados linha 1
        Label(dadosPaciente, text="Nome").grid(row=1, column=0, sticky="W", padx=3, pady=3)
        self.eNome = Entry(dadosPaciente)
        self.eNome.grid(row=1, column=1, columnspan=7, sticky=W+E, padx=3, pady=3)

        # Dados linha 2
        Label(dadosPaciente, text="Data de nascimento").grid(row=2, column=0, sticky="W", padx=3, pady=3)
        self.eNascimento = Entry(dadosPaciente, width=10)
        self.eNascimento.grid(row=2, column=1, sticky=W+E, padx=3, pady=3)
        Label(dadosPaciente, text="Sexo").grid(row=2, column=2, sticky=W+E, padx=3, pady=3)
        self.vSexo = StringVar()
        self.vSexo.set("M")
        self.radioM = Radiobutton(dadosPaciente, text="Masculino", variable=self.vSexo, value="M")
        self.radioM.grid(row=2, column=3, sticky=W+E, padx=3, pady=3)
        self.radioF = Radiobutton(dadosPaciente, text="Feminino", variable=self.vSexo, value="F")
        self.radioF.grid(row=2, column=4, sticky=W+E, padx=3, pady=3)
        Label(dadosPaciente, text="Estado civil").grid(row=2, column=5, sticky=W+E, padx=3, pady=3)
        self.comboECivil = ttk.Combobox(dadosPaciente, state='readonly', width=10)
        self.comboECivil.grid(row=2, column=6, columnspan=2, sticky=W+E, padx=3, pady=3)
        self.comboECivil['values'] = [ \
                'Solteiro',
                'Casado',
                'Divorciado',
                'Separado',
                'Viúvo',
                ]

        # Dados linha 3
        Label(dadosPaciente, text="Profisão").grid(row=3, column=0, sticky="W", padx=3, pady=3)
        self.eProfisao = Entry(dadosPaciente)
        self.eProfisao.grid(row=3, column=1, columnspan=4, sticky=W + E, padx=3, pady=3)
        Label(dadosPaciente, text="Telefone").grid(row=3, column=5, sticky="W", padx=3, pady=3)
        self.eTelefone = Entry(dadosPaciente, width=15)
        self.eTelefone.grid(row=3, column=6, sticky=W + E, padx=3, pady=3)

        # Dados linha 4
        fAnamnese = Frame(dadosPaciente, border=1, relief="groove")
        fAnamnese.grid(row=4, column=0, columnspan=7, sticky=W, padx=3, pady=3)
        Label(fAnamnese, text="Anamnese", font='bold').grid(row=0, column=0, sticky=W, padx=3, pady=3)

        # Anamnese linha 1
        Label(fAnamnese, text="Possui problema de saúde?").grid(row=1, column=0, sticky=W, padx=3, pady=3)
        self.vPSaude = StringVar()
        self.vPSaude.set("N")
        self.radioSPSaude = Radiobutton(fAnamnese, text="Sim", variable=self.vPSaude, value="S", command=self._changePSaude)
        self.radioSPSaude.grid(row=1, column=1, sticky=W, padx=3, pady=3)
        self.radioNPSaude = Radiobutton(fAnamnese, text="Não", variable=self.vPSaude, value="N", command=self._changePSaude)
        self.radioNPSaude.grid(row=1, column=2, sticky=W, padx=3, pady=3)
        Label(fAnamnese, text="Qual?").grid(row=1, column=3, sticky=W, padx=3, pady=3)
        self.ePSaude = Entry(fAnamnese, width=27)
        self.ePSaude.config(state='disabled')
        self.ePSaude.grid(row=1, column=4, sticky=W + E, padx=3, pady=3)

        # Anamnese linha 2
        Label(fAnamnese, text="Usa algum medicamento?").grid(row=2, column=0, sticky=W, padx=3, pady=3)
        self.vMedicamento = StringVar()
        self.vMedicamento.set("N")
        self.radioSMedicamento = Radiobutton(fAnamnese, text="Sim", variable=self.vMedicamento, value="S", command=self._changeMedicamento)
        self.radioSMedicamento.grid(row=2, column=1, sticky=W, padx=3, pady=3)
        self.radioNMedicamento = Radiobutton(fAnamnese, text="Não", variable=self.vMedicamento, value="N", command=self._changeMedicamento)
        self.radioNMedicamento.grid(row=2, column=2, sticky=W, padx=3, pady=3)
        Label(fAnamnese, text="Qual?").grid(row=2, column=3, sticky=W, padx=3, pady=3)
        self.eMedicamento = Entry(fAnamnese)
        self.eMedicamento.config(state='disabled')
        self.eMedicamento.grid(row=2, column=4, sticky=W + E, padx=3, pady=3)

        # Anamnese linha 3
        Label(fAnamnese, text="Está sob algum tratamento médico?").grid(row=3, column=0, sticky=W, padx=3, pady=3)
        self.vTratamento = StringVar()
        self.vTratamento.set("N")
        self.radioSTratamento = Radiobutton(fAnamnese, text="Sim", variable=self.vTratamento, value="S", command=self._changeTratamento)
        self.radioSTratamento.grid(row=3, column=1, sticky=W, padx=3, pady=3)
        self.radioNTratamento = Radiobutton(fAnamnese, text="Não", variable=self.vTratamento, value="N", command=self._changeTratamento)
        self.radioNTratamento.grid(row=3, column=2, sticky=W, padx=3, pady=3)
        Label(fAnamnese, text="Por que?").grid(row=3, column=3, sticky=W, padx=3, pady=3)
        self.eTratamento = Entry(fAnamnese)
        self.eTratamento.config(state='disabled')
        self.eTratamento.grid(row=3, column=4, sticky=W + E, padx=3, pady=3)

        # Anamnese linha 4
        Label(fAnamnese, text="Possui alergia a algum medicamento?").grid(row=4, column=0, sticky=W, padx=3, pady=3)
        self.vAlergia = StringVar()
        self.vAlergia.set("N")
        self.radioSAlergia = Radiobutton(fAnamnese, text="Sim", variable=self.vAlergia, value="S", command=self._changeAlergia)
        self.radioSAlergia.grid(row=4, column=1, sticky=W, padx=3, pady=3)
        self.radioNAlergia = Radiobutton(fAnamnese, text="Não", variable=self.vAlergia, value="N", command=self._changeAlergia)
        self.radioNAlergia.grid(row=4, column=2, sticky=W, padx=3, pady=3)
        Label(fAnamnese, text="Qual?").grid(row=4, column=3, sticky=W, padx=3, pady=3)
        self.eAlergia = Entry(fAnamnese)
        self.eAlergia.config(state='disabled')
        self.eAlergia.grid(row=4, column=4, sticky=W + E, padx=3, pady=3)

        # Anamnese linha 5
        Label(fAnamnese, text="Usa lentes corretivas?").grid(row=5, column=0, sticky="W", padx=3, pady=3)
        self.vLentes = StringVar()
        self.vLentes.set("N")
        self.radioLLentes = Radiobutton(fAnamnese, text="Lentes", variable=self.vLentes, value="L")
        self.radioLLentes.grid(row=5, column=1, sticky=W, padx=3, pady=3)
        self.radioOLentes = Radiobutton(fAnamnese, text="Óculos", variable=self.vLentes, value="O")
        self.radioOLentes.grid(row=5, column=2, sticky=W, padx=3, pady=3)
        self.radioNLentes = Radiobutton(fAnamnese, text="Não", variable=self.vLentes, value="N")
        self.radioNLentes.grid(row=5, column=3, sticky=W, padx=3, pady=3)

        observacao = Frame(dados, border=1, relief="groove")
        observacao.grid(row=0, column=1, sticky=E, padx=3, pady=3)
        Label(observacao, text="Observações").grid(row=0, column=0, columnspan=3, sticky=W, padx=3, pady=3)
        self.tObservacao = Text(observacao, height=17, width=18)
        self.tObservacao.grid(row=1, column=0, columnspan=3, sticky=W+E, padx=3, pady=3)

        exame = Frame(dados, border=1, relief="groove")
        exame.grid(row=1, column=0, columnspan=2, sticky=W+E, padx=3, pady=3)
        Label(exame, text="Exame").grid(row=0, column=0, columnspan=3, sticky="W", padx=3, pady=3)
        
        Label(exame, text="Local").grid(row=1, column=0, sticky="W", padx=3, pady=3)
        self.vDirectory = StringVar()

        if os.path.exists(exam['saveLocation']):
            self.vDirectory.set(exam['saveLocation'])
        else:
            self.vDirectory.set(os.getcwd())    
                 
        self.directory = Entry(exame, textvariable=self.vDirectory, width=88,  state="readonly")
        self.directory.grid(row=1, column=1, sticky=E + W, padx=3, pady=3)
        self.bPath = Button(exame, text="Localizar", command=lambda: self._path())
        self.bPath.grid(row=1, column=2, sticky=E, padx=3, pady=3)
        
        # __________________________________________________________________________________________________________
        # Frame Botões
        buttons = Frame(root)
        buttons.pack(side="bottom", fill="x")

        # Botão de gravar e preview
        self.gravar = Button(buttons, text="Iniciar gravação", command=lambda: self._gravar())
        self.gravar.pack(side="right", fill="y", expand=False, padx=5, pady=5)
        self.preview = Button(buttons, text="Preview", command=lambda: self._preview())
        self.preview.pack(side="right", fill="y", expand=False, padx=5, pady=5)

        # Segundos
        self.v_seg = StringVar()
        self.v_seg.set(exam['exSeg'])
        Label(buttons, text="seg").pack(side="right", fill="y", expand=False, padx=5, pady=5)
        self.eSeg = Entry(buttons, width=3, textvariable=self.v_seg)
        self.eSeg.pack(side="right", fill="y", expand=False, padx=5, pady=5)

        # Minutos
        self.v_min = StringVar()
        self.v_min.set(exam['exMin'])
        Label(buttons, text="min").pack(side="right", fill="y", expand=False, padx=5, pady=5)
        self.eMin = Entry(buttons, width=3, textvariable=self.v_min)
        self.eMin.pack(side="right", fill="y", expand=False, padx=5, pady=5)

        Label(buttons, text="Tempo de exposição").pack(side="right", fill="y", expand=False, padx=5, pady=5)


        # __________________________________________________________________________________________________________
        # Configuração dos pinos de IO do Raspberry
        # Configura para não mostrar alertas
        gpio.setwarnings(False)

        # Configurando GPIO
        gpio.setmode(gpio.BOARD)
        gpio.setup(38, gpio.OUT)
        gpio.setup(40, gpio.OUT)

        # Configurando o PWM com os valores iniciais de frequencia e dutycicle
        self.pwmIr = gpio.PWM(38, 200)
        self.pwmIr.start(0)
        self.pwmWhite = gpio.PWM(40, 200)
        self.pwmWhite.start(0)

    def _checkAnonimo(self):
        if self.pacienteAnonimo.get():
            self.eNome.delete(0, END)
            self.eNome.config(state='disabled')
            self.eNascimento.delete(0, END)
            self.eNascimento.config(state='disabled')
            self.vSexo.set("M")
            self.radioM.config(state='disabled')
            self.radioF.config(state='disabled')
            self.comboECivil.set("")
            self.comboECivil.config(state='disabled')
            self.eProfisao.delete(0, END)
            self.eProfisao.config(state='disabled')
            self.eTelefone.delete(0, END)
            self.eTelefone.config(state='disabled')
            self.vPSaude.set("N")
            self.radioSPSaude.config(state='disabled')
            self.radioNPSaude.config(state='disabled')
            self.ePSaude.delete(0, END)
            self.ePSaude.config(state='disabled')
            self.vMedicamento.set("N")
            self.radioSMedicamento.config(state='disabled')
            self.radioNMedicamento.config(state='disabled')
            self.eMedicamento.delete(0, END)
            self.eMedicamento.config(state='disabled')
            self.vTratamento.set("N")
            self.radioSTratamento.config(state='disabled')
            self.radioNTratamento.config(state='disabled')
            self.eTratamento.delete(0, END)
            self.eTratamento.config(state='disabled')
            self.vAlergia.set("N")
            self.radioSAlergia.config(state='disabled')
            self.radioNAlergia.config(state='disabled')
            self.eAlergia.delete(0, END)
            self.eAlergia.config(state='disabled')
            self.vLentes.set("N")
            self.radioLLentes.config(state='disabled')
            self.radioOLentes.config(state='disabled')
            self.radioNLentes.config(state='disabled')

        else:
            self.eNome.config(state='normal')
            self.eNascimento.config(state='normal')
            self.radioM.config(state='normal')
            self.radioF.config(state='normal')
            self.comboECivil.config(state='normal')
            self.eProfisao.config(state='normal')
            self.eTelefone.config(state='normal')
            self.radioSPSaude.config(state='normal')
            self.radioNPSaude.config(state='normal')
            self.radioSMedicamento.config(state='normal')
            self.radioNMedicamento.config(state='normal')
            self.radioSTratamento.config(state='normal')
            self.radioNTratamento.config(state='normal')
            self.radioSAlergia.config(state='normal')
            self.radioNAlergia.config(state='normal')
            self.radioLLentes.config(state='normal')
            self.radioOLentes.config(state='normal')
            self.radioNLentes.config(state='normal')

    def _changePSaude(self):
        if self.vPSaude.get() is "S":
            self.ePSaude.config(state='normal')
        else:
            self.ePSaude.delete(0, END)
            self.ePSaude.config(state='disabled')

    def _changeMedicamento(self):
        if self.vMedicamento.get() is "S":
            self.eMedicamento.config(state='normal')
        else:
            self.eMedicamento.delete(0, END)
            self.eMedicamento.config(state='disabled')

    def _changeTratamento(self):
        if self.vTratamento.get() is "S":
            self.eTratamento.config(state='normal')
        else:
            self.eTratamento.delete(0, END)
            self.eTratamento.config(state='disabled')

    def _changeAlergia(self):
        if self.vAlergia.get() is "S":
            self.eAlergia.config(state='normal')
        else:
            self.eAlergia.delete(0, END)
            self.eAlergia.config(state='disabled')

    def _path(self):
        directory = messagebox.filedialog.askdirectory()
        if len(directory) > 0:
            self.vDirectory.set(directory)
        else:
            if os.path.exists(exam['saveLocation']):
                self.vDirectory.set(exam['saveLocation'])
            else:
                self.vDirectory.set(os.getcwd())            

    def _validate(self):
        # Verifica se é paciente anônimo
        if not self.pacienteAnonimo.get():
            if(self.eNome.get() == ""):
                messagebox.showerror("Erro", "Nome é um campo obrigatório!")
                self.eNome.focus_set()
                return False

            if (self.eNascimento.get() == ""):
                messagebox.showerror("Erro", "Data de nascimento é um campo obrigatório!")
                self.eNascimento.focus_set()
                return False

            if (self.comboECivil.get() == ""):
                messagebox.showerror("Erro", "Estado civil é um campo obrigatório!")
                self.comboECivil.focus_set()
                return False

            if (self.eProfisao.get() == ""):
                messagebox.showerror("Erro", "Profisão é um campo obrigatório!")
                self.eProfisao.focus_set()
                return False

            if (self.eTelefone.get() == ""):
                messagebox.showerror("Erro", "Telefone é um campo obrigatório!")
                self.eTelefone.focus_set()
                return False

            if(self.vPSaude.get() == "S" and self.ePSaude.get() == ""):
                messagebox.showerror("Erro", "Expecificar o problema de saúde")
                self.ePSaude.focus_set()
                return False

            if(self.vMedicamento.get() == "S" and self.eMedicamento.get() == ""):
                messagebox.showerror("Erro", "Expecificar o medicamento")
                self.eMedicamento.focus_set()
                return False

            if (self.vTratamento.get() == "S" and self.eTratamento.get() == ""):
                messagebox.showerror("Erro", "Expecificar o tratamento")
                self.eTratamento.focus_set()
                return False

            if (self.vAlergia.get() == "S" and self.eAlergia.get() == ""):
                messagebox.showerror("Erro", "Expecificar qual medicament possui alergia")
                self.eAlergia.focus_set()
                return False

        if (self.v_min.get() == ""):
            messagebox.showerror("Erro", "O campo de minutos é obrigatório")
            self.eMin.focus_set()
            return False

        if not util.validateInt(self.v_min.get()):
            messagebox.showerror("Erro", "O campo de minutos deve ser inteiro")
            self.eMin.focus_set()
            return False

        if int(self.v_min.get()) < 0:
            messagebox.showerror("Erro", "O campo de minutos deve ser maior ou igual a zero")
            self.eMin.focus_set()
            return False

        if (self.v_seg.get() == ""):
            messagebox.showerror("Erro", "O campo de segundos é obrigatório")
            self.eSeg.focus_set()
            return False

        if not util.validateInt(self.v_seg.get()):
            messagebox.showerror("Erro", "O campo de segundos deve ser inteiro")
            self.eSeg.focus_set()
            return False

        if int(self.v_seg.get()) < 0:
            messagebox.showerror("Erro", "O campo de segundos deve ser maior ou igual a zero")
            self.eSeg.focus_set()
            return False

        if int(self.v_seg.get()) == 0 and int(self.v_min.get()) < 0:
            messagebox.showerror("Erro", "Os campos minuto e segundos não podem ser ambos zero")
            self.eSeg.focus_set()
            return False

        return True

    def _preview(self):
        PreviewConfig(self, self.pwmIr, self.pwmWhite)

    def _gravar(self):
        global exam
        
        if(self._validate()):
            exam = util.getExam()
            config = util.getConfig()
                
            exam['saveLocation'] = self.vDirectory.get()
            exam['exMin'] = self.v_min.get()
            exam['exSeg'] = self.v_seg.get()

            tempo = int(self.v_min.get()) * 60 + int(self.v_seg.get())

            util.setExam(exam)

            red = exam['rColor']
            green = exam['gColor']
            blue = exam['bColor']

            y = float(0.299 * red) + float(0.587 * green) + float(0.114 * blue)
            u = float(0.492 * (blue - y))
            v = float(0.877 * (red - y))

            if (platform.system() == "Linux"):
                self.pwmIr.ChangeDutyCycle(exam['ledIr'])
                self.pwmWhite.ChangeDutyCycle(exam['ledBr'])

                with picamera.PiCamera() as camera:
                    camera.sensor_mode = exam["cameraMode"]
                    for key in config['resolutions']:
                        if key['resName'] == "Mode " + str(exam["cameraMode"]):
                            camera.resolution = (key['width'], key['height'])
                            
                    camera.framerate = exam['fps']

                    camera.brightness = exam['brilho']
                    camera.contrast = exam['contraste']
                    camera.sharpness = exam['nitidez']
                    camera.saturation = exam['saturacao']
                    if exam['colorEfect']:
                        camera.color_effects = (u, v)
                    
        
                    camera.start_preview()
                    camera.start_recording('temp.h264')
                    camera.wait_recording(tempo)
                    camera.stop_recording()
                    camera.stop_preview()
                    camera.close()

                self.pwmIr.ChangeDutyCycle(0)
                self.pwmWhite.ChangeDutyCycle(0)

                now = datetime.now()
                nowstr = now.strftime("%Y-%m-%d %H:%M:%S")

                command = "MP4Box -fps %d -add temp.h264 exame.mp4" % (exam['fps'])
                subprocess.check_output(command, shell=True)

                location = os.getcwd() + '/temp.h264'
                os.remove(location)  # remove o arquivo temporario
                
                location = os.getcwd() + '/exame.mp4'
                
                if os.path.isfile("exame.mp4"):
                    result = messagebox.askquestion("Salvar", "Deseja salvar o arquivo?")
                    if result == 'yes':
                        nowstr = now.strftime("%Y%m%d%H%M%S")
                        pasta = exam['saveLocation']+'/'+nowstr
                        os.mkdir(pasta)
                        os.link("exame.mp4", str(pasta+"/exame.mp4"))
                        
                    os.remove(location)  # remove o arquivo temporario

                    # Cria arquivo de dados
                    dados = {
                        # Dados da aquisição
                        "data": now.strftime("%Y-%m-%d"),
                        "hora": now.strftime("%H:%M:%S"),
                        "ledIr": exam["ledIr"],
                        "ledBr": exam["ledBr"],
                        "contraste": exam["contraste"],
                        "saturacao": exam["saturacao"],
                        "nitidez": exam["nitidez"],
                        "brilho": exam["brilho"],
                        "cameraMode": exam["cameraMode"],
                        "fps": exam['fps'],
                        "colorEfect": exam['colorEfect'],
                        "rColor": exam['rColor'],
                        "bColor": exam['gColor'],
                        "gColor": exam['bColor'],

                        # Dados do paciente
                        "pacienteAnonimo": self.pacienteAnonimo.get(),
                        "nome": self.eNome.get(),
                        "dataNascimento": self.eNascimento.get(),
                        "sexo": self.vSexo.get(),
                        "estadoCivil": self.comboECivil.get(),
                        "profisao": self.eProfisao.get(),
                        "telefone": self.eTelefone.get(),
                        "problemaSaude": self.vPSaude.get(),
                        "tProblemaSaude": self.ePSaude.get(),
                        "medicamento": self.vMedicamento.get(),
                        "tMedicamento": self.eMedicamento.get(),
                        "tratamento": self.vTratamento.get(),
                        "tTratamento": self.eTratamento.get(),
                        "alergia": self.vAlergia.get(),
                        "tAlergia": self.eAlergia.get(),
                        "lentes": self.vLentes.get(),

                        # Obsercações
                        "observacoes": self.tObservacao.get("1.0", END)
                    }
                    util.setDados(pasta, dados)

                else:
                    messagebox.showerror("Erro", "Algo deu errado na gravação do arquivo")

            else:
                print("Faria um vídeo de ", tempo, " segundos se estivesse no raspberry")
