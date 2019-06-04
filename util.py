import cv2
import numpy
import json
from PIL import Image, ImageTk

def findPupila(frame, line=1):

    # Ver isso aqui
    # https://docs.opencv.org/3.0-beta/doc/py_tutorials/py_imgproc/py_houghcircles/py_houghcircles.html

    original = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  #converte para escala de cinza
    ret, imgBinarizadaReflexo = cv2.threshold(original, 35, 255, cv2.THRESH_BINARY) # extrai o reflexo

    elementoEstruturante = cv2.getStructuringElement(
        cv2.MORPH_ELLIPSE, (25, 25)
    )
    imBinRefEst = cv2.morphologyEx(imgBinarizadaReflexo, cv2.MORPH_OPEN, elementoEstruturante)

    sub = cv2.subtract(imBinRefEst, original)

    media = cv2.medianBlur(sub, 17)

    invert = cv2.bitwise_not(media)

    ret, imBinPipu = cv2.threshold(invert, 200, 255, cv2.THRESH_BINARY)

    # Desenhando um circulo e retas
    final = frame

    modo = cv2.RETR_TREE;
    metodo = cv2.CHAIN_APPROX_SIMPLE;
    _, contornos, hierarquia = cv2.findContours(imBinPipu, modo, metodo)

    # Arrumar isso aqui para pegar contornos circulares
    if(int(len(contornos[0]) > 4)):
        ellipse = cv2.fitEllipse(contornos[0])
        cv2.ellipse(final, ellipse, (0, 0, 255), line)

        centroX = int(ellipse[0][0])
        centroY = int(ellipse[0][1])
        width, height = frame.shape[:2]

        # linha horizontal
        cv2.line(final, (centroX, 0), (centroX, width), (0, 0, 255), line)
        # linha vertical
        cv2.line(final, (0, centroY), (height, centroY), (0, 0, 255), line)

        return centroX, centroY, final
    else:
        return 0, 0, final

def convertToExibe(frame, x=0, y=0):
    if ((x == 0) or (y == 0)):
        y = numpy.size(frame, 0)
        x = numpy.size(frame, 1)
    frame = cv2.resize(frame, (int(x), int(y)))
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    frame = ImageTk.PhotoImage(image=Image.fromarray(frame))
    return frame

def getConfig():
    global config
    with open('configs.json') as json_file:
        config = json.load(json_file)
    return config

def setConfig(config):
    with open('configs.json', 'w') as outfile:
        json.dump(config, outfile)

def getExam():
    global exam
    with open('exam.json') as json_file:
        exam = json.load(json_file)
    return exam

def setExam(exam):
    with open('exam.json', 'w') as outfile:
        json.dump(exam, outfile)

def setDados(location, dados):
    with open(location + '/dados.json', 'w') as outfile:
        json.dump(dados, outfile)

def getDados(location):
    global dados
    with open(location+'/dados.json') as json_file:
        dados = json.load(json_file)
    return dados

def validateInt(value):
    try:
        v = int(value)
        return True
    except ValueError:
        return False

def validateFloat(value):
    try:
        v = float(value)
        return value
    except ValueError:
        return None
