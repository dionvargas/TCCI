import util
from tkinter import *
from tkinter import ttk
from picamera import PiCamera

class PreviewConfig:


    def __init__(self, father, pwmIr, pwmWhite):

        exam = util.getExam()
        config = util.getConfig()

        # ____ JANELA DE PREVIEW
        self.camera = PiCamera()
        self.widthWindowPreview = 640
        self.heightWindowPreview = 480
        self.yControl = int((exam['monitorHeight']/2) - (self.heightWindowPreview/2) - 135)
        self.xControl = int((exam['monitorWidth']/2) - (self.widthWindowPreview/2))

        for key in config['resolutions']:
            if key['resName'] == "Mode " + str(exam["cameraMode"]):
                self.camera.sensor_mode = exam["cameraMode"]
                self.camera.resolution = (key['width'], key['height'])
        self.camera.start_preview(fullscreen=False, window=(self.xControl, self.yControl, self.widthWindowPreview, self.heightWindowPreview))

        # ____ JANELA DE CONTROLES

        widthWindowControl = 832
        heightWindowControl = 230
        yControl = int((exam['monitorHeight']/2) - (heightWindowControl/2) + 230)
        xControl = int((exam['monitorWidth']/2) - (widthWindowControl/2))

        self.window = Toplevel()
        self.window.title("Preview")
        self.window.minsize(widthWindowControl, heightWindowControl)
        self.window.geometry('{}x{}+{}+{}'.format(widthWindowControl, heightWindowControl, xControl, yControl))
        self.window.resizable(False, False)
        self.window.config(padx=5, pady=5)
        self.window.transient(father)
        self.window.focus_force()
        self.window.grab_set()

        self.pwmIr = pwmIr
        self.pwmWhite = pwmWhite

        self.root = Frame(self.window)
        self.root.pack(fill="both", expand="True")

        # Frame dos controles
        f_controles = Frame(self.root, bg="blue")
        f_controles.grid(column=0, row=0, sticky=N + S + E + W)

        # Coluna de controle dos leds
        f_led = Frame(f_controles, border = 1, relief="groove")
        f_led.grid(column=0, row=0)
        Label(f_led, text="Luminosidade").grid(row=0, column=0, columnspan=4, padx=5, pady=5)
        
        Label(f_led, text="IR").grid(column=0, row=1, sticky=N + S + E + W, padx=5, pady=5)
        self.irScale = Scale(f_led, from_=0, to=100, showvalue="False", orient="horizontal", command=self.ledIrChange)
        self.irScale.grid(column=1, row=1, sticky=N + S + E + W, padx=5, pady=5)
        self.irScale.set(exam['ledIr'])
        self.irValue = Label(f_led, text="%03d" % exam['ledIr'])
        self.irValue.grid(column=2, row=1, sticky=N + S + E + W, padx=5, pady=5)
        
        Label(f_led, text="BR").grid(column=0, row=2, sticky=N + S + E + W, padx=5, pady=5)
        self.brScale = Scale(f_led, from_=0, to=100, showvalue="False", orient="horizontal", command=self.ledBrChange)
        self.brScale.grid(column=1, row=2, sticky=N + S + E + W, padx=5, pady=5)
        self.brScale.set(exam['ledBr'])
        self.brValue = Label(f_led, text="%03d" % exam['ledBr'])
        self.brValue.grid(column=2, row=2, sticky=N + S + E + W, padx=5, pady=5)

        # Coluna de controles rápidos
        fFast = Frame(f_controles, border = 1, relief="groove")
        fFast.grid(column=1, row=0)
        Label(fFast, text="Controles Rápidos").grid(row=0, column=0, columnspan=6, padx=5, pady=5)
        
        Label(fFast, text="Brilho").grid(column=0, row=1, sticky=N + S + E + W, padx=5, pady=5)
        self.brilhoScale = Scale(fFast, from_=0, to=100, showvalue="False", orient="horizontal", command=self.brilhoChange)
        self.brilhoScale.grid(column=1, row=1, sticky=N + S + E + W, padx=5, pady=5)
        self.brilhoScale.set(exam['brilho'])
        self.brilhoValue = Label(fFast, text="%03d" % exam['brilho'])
        self.brilhoValue.grid(column=2, row=1, sticky=N + S + E + W, padx=5, pady=5)
        
        Label(fFast, text="Contraste").grid(column=0, row=2, sticky=N + S + E + W, padx=5, pady=5)
        self.contrasteScale = Scale(fFast, from_=0, to=100, showvalue="False", orient="horizontal", command=self.contrasteChange)
        self.contrasteScale.grid(column=1, row=2, sticky=N + S + E + W, padx=5, pady=5)
        self.contrasteScale.set(exam['contraste'])
        self.contrasteValue = Label(fFast, text="%03d" % exam['contraste'])
        self.contrasteValue.grid(column=2, row=2, sticky=N + S + E + W, padx=5, pady=5)

        Label(fFast, text="Saturação").grid(column=3, row=1, sticky=N + S + E + W, padx=5, pady=5)
        self.saturacaoScale = Scale(fFast, from_=0, to=100, showvalue="False", orient="horizontal", command=self.saturacaoChange)
        self.saturacaoScale.grid(column=4, row=1, sticky=N + S + E + W, padx=5, pady=5)
        self.saturacaoScale.set(exam['saturacao'])
        self.saturacaoValue = Label(fFast, text="%03d" % exam['saturacao'])
        self.saturacaoValue.grid(column=5, row=1, sticky=N + S + E + W, padx=5, pady=5)
        
        Label(fFast, text="Nitidez").grid(column=3, row=2, sticky=N + S + E + W, padx=5, pady=5)
        self.nitidezScale = Scale(fFast, from_=0, to=100, showvalue="False", orient="horizontal", command=self.nitidezChange)
        self.nitidezScale.grid(column=4, row=2, sticky=N + S + E + W, padx=5, pady=5)
        self.nitidezScale.set(exam['nitidez'])
        self.nitidezValue = Label(fFast, text="%03d" % exam['nitidez'])
        self.nitidezValue.grid(column=5, row=2, sticky=N + S + E + W, padx=5, pady=5)

        # Coluna de cores
        fCores = Frame(f_controles, border=1, relief="groove")
        fCores.grid(column=3, row=0, rowspan=2, sticky=N + S + E + W)
        Label(fCores, text="Controle de cores").grid(row=0, column=0, columnspan=6, padx=5, pady=5)

        self.vCor = BooleanVar()
        self.checkCores = Checkbutton(fCores, text="Filtro de cores", var=self.vCor, offvalue=False, onvalue=True, command=self.enableCores)
        self.checkCores.grid(column=0, row=1, columnspan=3, sticky=N + S + E + W)

        Label(fCores, text="R").grid(column=0, row=2, sticky=N + S + E + W, padx=5, pady=5)
        self.rScale = Scale(fCores, from_=0, to=255, showvalue="False", orient="horizontal", command=self.rChange)
        self.rScale.grid(column=1, row=2, sticky=N + S + E + W, padx=5, pady=5)
        self.rScale.set(exam['rColor'])
        self.rValue = Label(fCores, text="%03d" % exam['rColor'])
        self.rValue.grid(column=2, row=2, sticky=N + S + E + W, padx=5, pady=5)

        Label(fCores, text="G").grid(column=0, row=3, sticky=N + S + E + W, padx=5, pady=5)
        self.gScale = Scale(fCores, from_=0, to=255, showvalue="False", orient="horizontal", command=self.gChange)
        self.gScale.grid(column=1, row=3, sticky=N + S + E + W, padx=5, pady=5)
        self.gScale.set(exam['gColor'])
        self.gValue = Label(fCores, text="%03d" % exam['gColor'])
        self.gValue.grid(column=2, row=3, sticky=N + S + E + W, padx=5, pady=5)

        Label(fCores, text="B").grid(column=0, row=4, sticky=N + S + E + W, padx=5, pady=5)
        self.bScale = Scale(fCores, from_=0, to=255, showvalue="False", orient="horizontal", command=self.bChange)
        self.bScale.grid(column=1, row=4, sticky=N + S + E + W, padx=5, pady=5)
        self.bScale.set(exam['bColor'])
        self.bValue = Label(fCores, text="%03d" % exam['bColor'])
        self.bValue.grid(column=2, row=4, sticky=N + S + E + W, padx=5, pady=5)

        self.canvasCor = Canvas(fCores, width=20, height=20)
        self.canvasCor.grid(column=0, row=5, columnspan=3, sticky=N + S + E + W, padx=5, pady=5)
        self.updateCanvasCor(exam['rColor'], exam['gColor'], exam['bColor'])

        if exam['colorEfect'] is True:
            self.checkCores.select()
            self.vCor.set(True)
            
        else:
            self.checkCores.deselect()
            self.vCor.set(False)
            
        self.enableCores()

        # Linha de captura
        fCaptura = Frame(f_controles, border=1, relief="groove")
        fCaptura.grid(column=0, row=1, columnspan=2, sticky=N + S + E + W)
        Label(fCaptura, text="Captura").grid(row=0, column=0, columnspan=6, padx=5, pady=5)
        
        Label(fCaptura, text="Modo de captura").grid(row=1, column=0, sticky="W", padx=3, pady=3)
        self.SensorModeCombo = ttk.Combobox(fCaptura,state='readonly',width=60)
        self.SensorModeCombo.grid(row=1, column=1, columnspan=2, sticky=W+E, padx=3, pady=3)
        self.SensorModeCombo['values'] = [ \
                'Mode 1: to 1920x1080 1-30 fps ',
                'Mode 2: to 2592x1944 1-15 fps Image',
                'Mode 3: to 2592x1944 0.1666-1 fps Image',
                'Mode 4: to 1296x972  1-42 fps',
                'Mode 5: to 1296x730  1-49 fps',
                'Mode 6: to 640x480   42.1-60 fps',
                'Mode 7: to 640x480   60.1-90 fps'
                ]
        self.SensorModeCombo.current(exam['cameraMode'] - 1)
        self.SensorModeCombo.bind('<<ComboboxSelected>>',self.sensorModeChanged)

        # FrameRate
        Label(fCaptura, text="Frame Rate:").grid(column=0, row=2, sticky=W, padx=3, pady=3)
        self.fpsScale = Scale(fCaptura, resolution=0.01, length=450, showvalue="False", orient="horizontal", command=self.fpsChange)
        self.fpsScale.grid(column=1, row=2, sticky=E + W, padx=5, pady=5)
        for key in config['resolutions']:
            if key['resName'] == "Mode " + str(self.SensorModeCombo.current() + 1):
                self.fpsScale.config(to=key['maxfps'], from_=key['minfps'])
        self.fpsScale.set(exam['fps'])
        self.fpsValue = Label(fCaptura, text=exam['fps'])
        self.fpsValue.grid(column=2, row=2, sticky=E, padx=5, pady=5)
        
        #Frame dos botões
        fButtons = Frame(self.root)
        fButtons.grid(column=0, row=1, pady=5)
        self.cancelar = Button(fButtons, text="Descartar configurações", command=lambda: self._close()).grid(column=0, row=0, padx=5, pady=5)
        self.gravar = Button(fButtons, text="Salvar Configurações", command=lambda: self._salvar()).grid(column=1, row=0, padx=5, pady=5)
        
        self.window.protocol("WM_DELETE_WINDOW", self._close)
        self.window.mainloop()


    def enableCores(self):
        if self.vCor.get():
            self.rScale.config(state=NORMAL)
            self.gScale.config(state=NORMAL)
            self.bScale.config(state=NORMAL)
            self.yuvUpdate()
            
        else:
            self.rScale.config(state=DISABLED)
            self.gScale.config(state=DISABLED)
            self.bScale.config(state=DISABLED)
            self.camera.color_effects = None

    def updateMe(self,newVal, label):
        val = int(float(newVal))
        label.config(text="%03d" % val)
        return val

    def rChange(self, val):
        self.updateMe(val, self.rValue)
        self.yuvUpdate()

    def bChange(self, val):
        self.updateMe(val, self.bValue)
        self.yuvUpdate()

    def gChange(self, val):
        self.updateMe(val, self.gValue)
        self.yuvUpdate()

    def yuvUpdate(self):
        red = self.rScale.get()
        green = self.gScale.get()
        blue = self.bScale.get()
        self.updateCanvasCor(red, green, blue)

        u = (((-38*red)-(74*green)+(112*blue)+128) >> 8) +128
        v = (((112*red)-(94*green)-(18*blue)+128) >> 8) +128

        print("U:", u, "V:", v)

        self.camera.color_effects = (u, v)

    def updateCanvasCor(self, red, green, blue):
        self.canvasCor.config(background='#%02x%02x%02x' % (red, green, blue))

    def brilhoChange(self, val):
        self.camera.brightness = self.updateMe(val, self.brilhoValue)
        
    def contrasteChange(self, val):
        self.camera.contrast = self.updateMe(val, self.contrasteValue)
        
    def nitidezChange(self, val):
        self.camera.sharpness = self.updateMe(val, self.nitidezValue)
        
    def saturacaoChange(self, val):
        self.camera.saturation = self.updateMe(val, self.saturacaoValue)

    def ledIrChange(self, val):
        self.pwmIr.ChangeDutyCycle(self.updateMe(val, self.irValue))

    def ledBrChange(self, val):
        self.pwmWhite.ChangeDutyCycle(self.updateMe(val, self.brValue))

    def fpsChange(self, newVal):
        val = float(newVal)
        self.fpsValue.config(text="%.2f" % val)
        return val

    def sensorModeChanged(self, event):
        global config

        self.camera.stop_preview()
        self.camera.sensor_mode = int(self.SensorModeCombo.current()) + 1
        for key in config['resolutions']:
            if key['resName'] == "Mode " + str(self.SensorModeCombo.current() + 1):
                self.fpsScale.config(to=key['maxfps'], from_=key['minfps'])
                self.fpsScale.set(key['maxfps'])
                self.fpsValue.config(text="%.2f" % key['maxfps'])
                
        self.camera.start_preview(fullscreen=False, window=(self.xControl, self.yControl, self.widthWindowPreview, self.heightWindowPreview))

    def _salvar(self):
        exam = util.getExam()

        # Salva os valores da captura
        exam['cameraMode'] = int(self.SensorModeCombo.current()) + 1
        exam['fps'] = self.fpsScale.get()
            
        # Salva os valores dos parametros da camera
        exam['contraste'] = self.contrasteScale.get()
        exam['nitidez'] = self.nitidezScale.get()
        exam['saturacao'] = self.saturacaoScale.get()
        exam['brilho'] = self.brilhoScale.get()    
            
        # Salva os valores dos leds
        exam['ledIr'] = self.irScale.get()
        exam['ledBr'] = self.brScale.get()

        # Salva valores dos filtros de Cor
        exam['colorEfect'] = self.vCor.get()
        exam['rColor'] = self.rScale.get()
        exam['gColor'] = self.gScale.get()
        exam['bColor'] = self.bScale.get()

        util.setExam(exam)

        self._close()

    def _close(self):
        # Desabilita a camera

        self.camera.stop_preview()
        self.camera.close()

        # Desliga os leds
        self.pwmIr.ChangeDutyCycle(0)
        self.pwmWhite.ChangeDutyCycle(0)


        # Fecha a janela
        self.window.destroy()
