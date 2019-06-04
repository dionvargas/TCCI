from tkinter import Frame
from tkinter import StringVar
from tkinter import Label


class EmptyContainer(Frame):

    def __init__(self):
        super().__init__()

        # ______________________________________________________________________________________________________________
        # Rodapé
        bottom = Frame(self, height=20);
        bottom.pack(side="bottom", fill="x")
        bottom.configure(relief="groove", border=3)
        self.l_footer = StringVar()
        footer = Label(bottom, textvariable=self.l_footer)
        footer.pack(side="left")