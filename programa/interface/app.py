import re
import tkinter as tk
from tkinter import ttk, messagebox

from interface.scrollbar import ScrollbarFrame
from interface.ativo_frame import AtivoFrame
from models.ativo import Ativo
from utils.constantes import CATEGORIAS

class App(tk.Tk):

    def __init__(self):
        super().__init__()

        self.title("Gerenciador de Ativos")
        self.geometry("900x700")

        self.ativos = []
        self.ids_existentes = set()
        self.frames_categorias = {}
        self.frames_ativos = {}

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
            text="Adicionar",
            command=self.adicionar_ativo
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

        self.entry_busca.bind(
            "<KeyRelease>",
            self.filtrar_ativos
        )

        self.categoria_filtro_var = tk.StringVar(
            value="Todas"
        )

        self.combo_filtro_categoria = ttk.Combobox(
            self.frame_busca,
            textvariable=self.categoria_filtro_var,
            values=["Todas"] + CATEGORIAS,
            state="readonly",
            width=18
        )

        self.combo_filtro_categoria.pack(
            side="left",
            padx=(10, 0)
        )

        self.combo_filtro_categoria.bind(
        "<<ComboboxSelected>>",
        self.filtrar_ativos
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

    def adicionar_ativo(self):

        identificador = self.entry_id.get().strip()
        categoria = self.categoria_var.get()

        if identificador =="":
            messagebox.showwarning(
                "Inválido",
                "Informe um identificador para o ativo."
            )
            return
        
        chave = (categoria, identificador)

        if chave in self.ids_existentes:
            messagebox.showwarning(
                "Inválido",
                f"Já existe um ativo com o ID '{identificador}' na categoria '{categoria}'."
            )
            return

        ativo = Ativo(
            identificador=identificador,
            categoria=categoria
        )

        frame = AtivoFrame(
            parent=self.frames_categorias[categoria],
            ativo=ativo,
            on_remover=self.remover_ativo
        )

        frame.pack(
            fill="x",
            padx=5,
            pady=5
        )

        self.ids_existentes.add(chave)
        self.frames_ativos[chave] = frame

        self.ativos.append(ativo)

        self.entry_id.delete(0, tk.END)

        self.filtrar_ativos()

    def remover_ativo(self, ativo):

        if ativo in self.ativos:
            self.ativos.remove(ativo)

        chave = (ativo.categoria, ativo.identificador)
        self.ids_existentes.discard(chave)
        frame = self.frames_ativos.pop(chave)

        frame.destroy()

        self.filtrar_ativos()

    def filtrar_ativos(self, event=None):

        termo = self.entry_busca.get().strip().lower()
        categoria_filtro = self.categoria_filtro_var.get()

        for categoria in CATEGORIAS:

            ativos_categoria = [
                ativo for ativo in self.ativos
                if ativo.categoria == categoria
            ]

            ativos_categoria.sort(
                key=lambda ativo: self.chave_ordenacao(ativo.identificador)
            )

            algum_visivel = False

            for ativo in ativos_categoria:

                chave = (ativo.categoria, ativo.identificador)
                frame = self.frames_ativos[chave]

                campos = [
                    ativo.identificador,
                    ativo.hostname,
                    ativo.responsavel,
                    ativo.setor
                ]

                corresponde_busca = any(
                    termo in campo.lower()
                    for campo in campos
                )

                corresponde_categoria = (
                    categoria_filtro == "Todas"
                    or ativo.categoria == categoria_filtro
                )

                frame.pack_forget()

                if corresponde_busca and corresponde_categoria:

                    frame.pack(
                        fill="x",
                        padx=5,
                        pady=5
                    )

                    algum_visivel = True

            frame_categoria = self.frames_categorias[categoria]

            if algum_visivel:

                if not frame_categoria.winfo_manager():

                    frame_categoria.pack(
                        fill="x",
                        padx=10,
                        pady=5
                    )

            else:

                frame_categoria.pack_forget()

    def chave_ordenacao(self, identificador):

        return[
            int(parte) if parte.isdigit() else parte.lower()
            for parte in re.split(r"(\d+)", identificador)
        ]