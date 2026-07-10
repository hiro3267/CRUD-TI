import tkinter as tk
from tkinter import ttk
from interface.vulnerabilidade_frame import VulnerabilidadeFrame
from models.ativo import Ativo
from models.vulnerabilidade import Vulnerabilidade
from utils.constantes import CORES_INDICADOR_ATIVO

class AtivoFrame(ttk.Frame):

    def __init__(self, parent, ativo: Ativo, on_remover):
        super().__init__(parent)

        self.ativo = ativo
        self.on_remover = on_remover
        self.vulnerabilidades = []
        self.frames_vulnerabilidades = {}

        self.label_titulo = tk.Label(
            self,
            text=f"Ativo: {ativo.identificador}",
            fg=CORES_INDICADOR_ATIVO["ok"]
        )

        self.container = ttk.Labelframe(
            self,
            labelwidget=self.label_titulo
        )

        self.container.pack(
            fill="x",
            expand=True
        )

        self.criar_widgets()

        self.atualizar_indicador()

    def criar_widgets(self):

        self.criar_frame_campos()
        self.criar_campos()

        self.criar_area_vulnerabilidades()

        self.criar_frame_botoes()
        self.criar_botoes()

    def criar_frame_campos(self):

        self.frame_campos = ttk.Frame(self.container)

        self.frame_campos.pack(
            fill="x",
            padx=10,
            pady=10
        )

    def criar_frame_botoes(self):
        
        self.frame_botoes = ttk.Frame(self.container)

        self.frame_botoes.pack(
            fill="x",
            padx=10,
            pady=(0, 10)
        )

    def criar_area_vulnerabilidades(self):

        self.frame_vulnerabilidades = ttk.LabelFrame(
            self.container,
        text="Vulnerabilidades"
        )

        self.frame_vulnerabilidades.pack(
            anchor="w",
            pady=(0, 5)
        )

    def criar_botoes(self):
        
        self.botao_add_vulnerabilidade = ttk.Button(
            self.frame_botoes,
            text="Adicionar Vulnerabilidade",
            command=self.adicionar_vulnerabilidade
        )

        self.botao_add_vulnerabilidade.pack(side="left")

        self.botao_excluir = ttk.Button(
            self.frame_botoes,
            text="Excluir Ativo",
            command=self.excluir
        )

        self.botao_excluir.pack(side="right")

    def criar_campos(self):

        self.criar_campo_hostname()
        self.criar_campo_responsavel()
        self.criar_campo_setor()

    def criar_campo_hostname(self):

        self.label_hostname = ttk.Label(
            self.frame_campos,
            text="Hostname:"
        )

        self.label_hostname.grid(
            row=0,
            column=0,
            padx=5,
            pady=5,
            sticky="w"
        )

        self.entry_hostname = ttk.Entry(self.frame_campos)

        self.entry_hostname.grid(
            row=0,
            column=1,
            padx=5,
            pady=5,
            sticky="ew"
        )

        self.entry_hostname.bind(
            "<KeyRelease>",
            self.atualizar_hostname
        )

        self.frame_campos.columnconfigure(1, weight=1)

    def criar_campo_responsavel(self):

        self.label_responsavel = ttk.Label(
            self.frame_campos,
            text="Responsável:"
        )

        self.label_responsavel.grid(
            row=1,
            column=0,
            padx=5,
            pady=5,
            sticky="w"
        )

        self.entry_responsavel = ttk.Entry(self.frame_campos)

        self.entry_responsavel.grid(
            row=1,
            column=1,
            padx=5,
            pady=5,
            sticky="ew"
        )

        self.entry_responsavel.bind(
            "<KeyRelease>",
            self.atualizar_responsavel
        )

    def criar_campo_setor(self):
        
        self.label_setor = ttk.Label(
            self.frame_campos,
            text="Setor:"
        )

        self.label_setor.grid(
            row=2,
            column=0,
            padx=5,
            pady=5,
            sticky="w"
        )

        self.entry_setor = ttk.Entry(self.frame_campos)

        self.entry_setor.grid(
            row=2,
            column=1,
            padx=5,
            pady=5,
            sticky="ew"
        )

        self.entry_setor.bind(
            "<KeyRelease>",
            self.atualizar_setor
        )

    def excluir(self):

        self.on_remover(self.ativo)

    def atualizar_hostname(self, event=None):

        self.ativo.hostname = self.entry_hostname.get().strip()

    def atualizar_responsavel(self, event=None):

        self.ativo.responsavel = self.entry_responsavel.get().strip()

    def atualizar_setor(self, event=None):

        self.ativo.setor = self.entry_setor.get().strip()

    def adicionar_vulnerabilidade(self):

        vulnerabilidade = Vulnerabilidade()

        self.ativo.vulnerabilidades.append(vulnerabilidade)
        self.vulnerabilidades.append(vulnerabilidade)

        frame = VulnerabilidadeFrame(
            parent=self.frame_vulnerabilidades,
            vulnerabilidade=vulnerabilidade,
            on_remover=self.remover_vulnerabilidade,
            on_mudanca=self.atualizar_indicador
        )

        frame.pack(
            fill="x",
            padx=5,
            pady=5
        )

        self.frames_vulnerabilidades[id(vulnerabilidade)] = frame

    def remover_vulnerabilidade(self, vulnerabilidade):

        if vulnerabilidade in self.ativo.vulnerabilidades:
            self.ativo.vulnerabilidades.remove(vulnerabilidade)

        if vulnerabilidade in self.vulnerabilidades:
            self.vulnerabilidades.remove(vulnerabilidade)

        frame = self.frames_vulnerabilidades.pop(id(vulnerabilidade))
        frame.destroy()

        self.atualizar_indicador()

    def atualizar_indicador(self):

        estados = [v.status for v in self.ativo.vulnerabilidades]

        if any(estado in ("Aberta", "Em Tratamento") for estado in estados):

            situacao = "risco"

        elif any(estado == "Aceita" for estado in estados):
            situacao = "aceita"

        else:
            situacao = "ok"

        self.container.configure(
            style=f"Indicador{situacao.capitalize()}.TLabelframe"
        )