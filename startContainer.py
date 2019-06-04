from emptyContainer import EmptyContainer
from tkinter import *
from PIL import Image, ImageTk

class StartContainer(EmptyContainer):

    def __init__(self):
        super().__init__()

        image = Image.open("resources/horus.png")
        image = image.resize((580, 168), Image.ANTIALIAS)
        imagem = ImageTk.PhotoImage(image)
        w = Label(self, image=imagem)
        w.imagem = imagem
        w.pack(expand=True)
