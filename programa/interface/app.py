import tkinter as tk
from tkinter import ttk

from interface.scrollbar import ScrollbarFrame
from utils.constantes import CATEGORIAS

class App(tk.Tk):

    def __init__(self):
        super().__init__()

        self.title("Gerenciador de Ativos")
        self.geometry("900x700")

        self.ativos = []
        self.ids_existentes = set()
        self.frames_categorias = {}

        self.criar_interface()

    def criar_interface(self):
        self.criar_frame_controle()
        self.criar_frame_busca()
        self.criar_scroll()
        self.criar_categorias()

    def criar_frame_controle(self):
        
        self.frame_controle = ttk.Frame(self)

        self.frame_controle.pack(
            fill="x",
            padx=10,
            pady=10
        )

        self.entry_id = ttk.Entry(self.frame_controle)

        self.entry_id.pack(
            side="left",
            padx=10,
            pady=10
        )

        self.categoria_var = tk.StringVar(
            value=CATEGORIAS[0]
        )

        self.combo_categoria = ttk.Combobox(
            self.frame_controle,
            textvariable=self.categoria_var,
            values=CATEGORIAS,
            state="readonly",
            width=18
        )

        self.combo_categoria.pack(
            side="left"
        )

        self.botao_adicionar = ttk.Button(
            self.frame_controle,
            text="Adicionar"
        )

        self.botao_adicionar.pack(
            side="left",
            padx=(10, 0)
        )

    def criar_frame_busca(self):
        

        self.frame_busca = ttk.Frame(self)

        self.frame_busca.pack(
            fill="x",
            padx=10,
            pady=(0, 10)
        )

        self.entry_busca = ttk.Entry(self.frame_busca)

        self.entry_busca.pack(
            fill="x",
            expand=True
        )

    def criar_scroll(self):

        self.scroll = ScrollbarFrame(self)
        
        self.scroll.pack(
            fill="both",
            expand=True,
            padx=10,
            pady=10
        )

    def criar_categorias(self):
        
        self.frames_categorias = {}

        for categoria in CATEGORIAS:

            frame = ttk.LabelFrame(
                self.scroll.content,
                text=categoria
            )

            frame.pack(
                fill="x",
                padx=10,
                pady=5
            )

            self.frames_categorias[categoria] = frame