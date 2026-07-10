import tkinter as tk
from tkinter import ttk, messagebox

from interface.scrollbar import ScrollbarFrame
from interface.ativo_frame import AtivoFrame
from models.ativo import Ativo
from services.filtro_service import FiltroService
from utils.constantes import CATEGORIAS, PREFIXOS_CATEGORIA

class App(tk.Tk):

    def __init__(self):
        super().__init__()

        self.title("Gerenciador de Ativos")
        self.geometry("900x700")

        self.ativos = []
        self.ids_existentes = set()
        self.frames_categorias = {}
        self.frames_ativos = {}
        self.contadores_categoria = {categoria: 0 for categoria in CATEGORIAS}

        self.criar_interface()

    def criar_interface(self):
        self.criar_frame_controle()
        self.criar_frame_busca()
        self.criar_scroll()
        self.criar_categorias()
        self.filtrar_ativos()

    def criar_frame_controle(self):
        
        self.frame_controle = ttk.Frame(self)

        self.frame_controle.pack(
            fill="x",
            padx=10,
            pady=10
        )

        self.entry_numero = ttk.Entry(self.frame_controle, width=10)

        self.entry_numero.pack(
            side="left",
            padx=(10, 10)
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

        self.entry_busca = ttk.Entry(self.frame_busca)

        self.entry_busca.pack(
            fill="x",
            expand=True
        )

        self.entry_busca.bind(
            "<KeyRelease>",
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

        categoria = self.categoria_var.get()
        prefixo = PREFIXOS_CATEGORIA[categoria]

        texto_numero = self.entry_numero.get().strip()

        if texto_numero =="":
            
            self.contadores_categoria[categoria] += 1
            numero = self.contadores_categoria[categoria]

        else:

            if not texto_numero.isdigit() or int(texto_numero) < 1:

                messagebox.showwarning(
                    "Inválido",
                    "O número do ID deve ser um inteiro positivo."
                )

                return
        
            numero = int(texto_numero)

            identificador = f"{prefixo}-{numero}"

            if (categoria, identificador) in self.ids_existentes:

                messagebox.showwarning(
                    "Duplicado",
                    f"Já existe um ativo com o ID '{identificador}'."
                )

                return
        
            if numero >= self.contadores_categoria[categoria]:

                self.contadores_categoria[categoria] = numero
        
        identificador = f"{prefixo}-{numero}"

        chave = (categoria, identificador)

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

        self.entry_numero.delete(0, tk.END)

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

        termo = self.entry_busca.get()
        categoria_filtro = self.categoria_filtro_var.get()

        for categoria in CATEGORIAS:

            ativos_categoria = FiltroService.filtrar_categoria(
                self.ativos,
                categoria,
                termo,
                categoria_filtro
            )

            algum_visivel = False

            for ativo, visivel in ativos_categoria:

                chave = (ativo.categoria, ativo.identificador)
                frame = self.frames_ativos[chave]

                frame.pack_forget()

                if visivel:

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
