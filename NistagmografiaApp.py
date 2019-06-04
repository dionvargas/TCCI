
import tkinter
import os
import platform
import util

from tkinter import *
from tkinter import filedialog
from screeninfo import get_monitors

from startContainer import StartContainer
from captureContainer import CaptureContainer
from playContainer import PlayContainer
from processaContainer import ProcessaContainer
from resultadoContainer import ResultadoContainer


class App:

    global config
    global exam

    def __init__(self, window, window_title):
        global exam
        
        exam = util.getExam()
        # Arrumar isso aqui
        for m in get_monitors():
            exam['monitorHeight'] = m.height
            exam['monitorWidth'] = m.width
        util.setExam(exam)

        widthWindow = 863
        heightWindow = 600
        y = int((exam['monitorHeight']/ 2) - (heightWindow/2))
        x = int((exam['monitorWidth']/ 2) - (widthWindow/2)) 

        self.window = window
        self.window.title(window_title)
        self.window.minsize(widthWindow, heightWindow)
        self.window.geometry('{}x{}+{}+{}'.format(widthWindow, heightWindow, x, y))
        #self.window.iconbitmap("/resources/icone.ico")
        #self.window.resizable(0,0)     # se quiser deixar sem poder redimencioar a janela

        # Barra de menus
        menuBar = Menu(self.window)
        self.window.config(menu=menuBar)
        fileMenu = Menu(menuBar, tearoff=0)
        menuBar.add_cascade(label="Arquivo", menu=fileMenu)
        fileMenu.add_command(label="Nova aquisição", command=self._novaAquisicao)
        fileMenu.add_command(label="Processar...", command=self._processa)
        fileMenu.add_separator()
        fileMenu.add_command(label="Abrir Vídeo...", command=self._abrir)
        fileMenu.add_command(label="Abrir Exame...", command=self._abrirExame)
        fileMenu.add_separator()
        fileMenu.add_command(label="Sair", command=self._quit)
        helpMenu = Menu(menuBar, tearoff=0)
        menuBar.add_cascade(label="Ajuda", menu=helpMenu)
        helpMenu.add_command(label="Sobre...", command=self._sobre)

        # Container
        self.container = StartContainer()
        self.container.pack(fill='both', expand=True)

        self.window.mainloop()

    def _abrir(self):
        openFile = filedialog.askopenfilename(initialdir=os.getcwd(), title="Selecione um arquivo", filetypes=(("Arquivos MP4", "*.mp4"), ("all files", "*.*")))

        if(len(openFile) != 0):
            self.container.destroy()
            self.container = PlayContainer(openFile)
            self.container.pack(fill='both', expand=True)

    def _abrirExame(self):
        openPath = filedialog.askdirectory()
        if (len(openPath) != 0):
            self._resultado(openPath)

    def _processa(self):
        openFile = filedialog.askopenfilename(initialdir=os.getcwd(), title="Selecione um arquivo",
                                              filetypes=(("Arquivos MP4", "*.mp4"), ("all files", "*.*")))
        if (len(openFile) != 0):
            self.container.destroy()
            self.container = ProcessaContainer(self,openFile)
            self.container.pack(fill='both', expand=True)

    def _resultado(self, directory):
        self.container.destroy()
        self.container = ResultadoContainer(self, directory)
        self.container.pack(fill='both', expand=True)

    def _novaAquisicao(self):
        self.container.destroy()
        self.container = CaptureContainer()
        self.container.pack(fill='both', expand=True)

    def _empty(self):
        self.container.destroy()
        self.container = StartContainer()
        self.container.pack(fill='both', expand=True)

    def _quit(self):
        self.window.quit()
        self.window.destroy()
        exit()

    def _sobre(self):
        print("Apertado o botão sobre!")

def run():
    global config
    global exam

    if(platform.system() == "Linux"):
        location = os.getcwd() + '/'
    else:
        location = os.getcwd() + '\\'

    if not os.path.isfile(location + "exam.json"):
        print("Criando arquivo exam.json")
        exam = {
            "monitorHeight": 0,
            "monitorWidth": 0,
            "ledIr": 0,
            "ledBr": 0,
            "contraste":0,
            "saturacao":0,
            "nitidez":0,
            "brilho":50,
            "cameraMode":7,
            "fps":90,
            "exMin": 0,
            "exSeg": 5,
            "saveLocation": os.getcwd(),
            "colorEfect": False,
            "rColor": 128,
            "bColor": 128,
            "gColor": 128
        }
        util.setExam(exam)

    if not os.path.isfile(location + "configs.json"):
        print("Criando arquivo configs.json")
        res = {}
        res['resolutions'] = []
        res['resolutions'].append({
            "resName": "Mode 1",
            "minfps": 1,
            "maxfps": 30,
            "width": 1920,
            "height": 1080
        })
        res['resolutions'].append({
            "resName": "Mode 2",
            "minfps": 1,
            "maxfps": 15,
            "width": 2592,
            "height": 1944
        })
        res['resolutions'].append({
            "resName": "Mode 3",
            "minfps": 0.17,
            "maxfps": 1,
            "width": 2592,
            "height": 1944
        })
        res['resolutions'].append({
            "resName": "Mode 4",
            "minfps": 1,
            "maxfps": 42,
            "width": 1296,
            "height": 972
        })
        res['resolutions'].append({
            "resName": "Mode 5",
            "minfps": 1,
            "maxfps": 49,
            "width": 640,
            "height": 480
        })
        res['resolutions'].append({
            "resName": "Mode 6",
            "minfps": 42.1,
            "maxfps": 60,
            "width": 1920,
            "height": 1080
        })
        res['resolutions'].append({
            "resName": "Mode 7",
            "minfps": 60.1,
            "maxfps": 90,
            "width": 640,
            "height": 480
        })

        ext = {}
        ext['extensions'] = []
        ext['extensions'].append({
            "extension": "MP4",
            "archive": ".mp4",
            "text": "Arquivos MP4"
        })

        configs = {
            'resolutions': res['resolutions'],
            'extensions': ext['extensions']
        }

        util.setConfig(configs)
      

    # Comando para poder usar a camera do raspberry como camera normal
    if (platform.system() == "Linux"):
        os.system('sudo modprobe bcm2835-v4l2')


    # Cria a janela e passa como parametro o objeto da aplicação
    App(tkinter.Tk(), "Sistema Hórus")

if __name__ == '__main__':
    print('running....')
    run()
