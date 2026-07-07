import tkinter as tk
from tkinter import ttk

from interface.scrollbar import ScrollbarFrame

class App(tk.Tk):

    def __init__(self):
        super().__init__()

        self.title("Gerenciador de Ativos")
        self.geometry("900x700")

        self.criar_interface()

    def criar_interface(self):
        self.criar_frame_controle()
        self.criar_frame_busca()
        self.criar_scroll()
        self.criar_categorias()

    def criar_frame_controle(self):
        pass

    def criar_frame_busca(self):
        pass

    def criar_scroll(self):

        self.scroll = ScrollbarFrame(self)
        
        self.scroll.pack(
            fill="both",
            expand=True,
            padx=10,
            pady=10
        )

    def criar_categorias(self):
        pass