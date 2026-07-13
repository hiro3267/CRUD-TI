import tkinter as tk
from tkinter import ttk
from models.vulnerabilidade import Vulnerabilidade
from utils.constantes import (TIPOS_VULNERABILIDADE, SEVERIDADES, STATUS_VULNERABILIDADES, CORES_SEVERIDADE)

class VulnerabilidadeFrame(ttk.Frame):

    def __init__(self, parent, vulnerabilidade: Vulnerabilidade, on_remover, on_mudanca=None):
        super().__init__(parent)

        self.vulnerabilidade = vulnerabilidade
        self.on_remover = on_remover
        self.on_mudanca = on_mudanca

        self.label_titulo = tk.Label(
            self,
            text="Vulnerabilidade",
            fg=CORES_SEVERIDADE[SEVERIDADES[0]]
        )

        self.container = ttk.LabelFrame(
            self,
            labelwidget=self.label_titulo
        )

        self.container.pack(
            fill="x",
            expand=True
        )

        self.criar_widgets()

    def criar_widgets(self):

        self.criar_frame_campos()
        self.criar_campos()

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

    def criar_campos(self):

        self.criar_campo_descricao()
        self.criar_campo_tipo()
        self.criar_campo_severidade()
        self.criar_campo_status()

    def criar_campo_descricao(self):

        self.label_descricao = ttk.Label(
            self.frame_campos,
            text="Descrição:"
        )

        self.label_descricao.grid(
            row=0,
            column=0,
            padx=5,
            pady=5,
            sticky="ew"
        )

        self.entry_descricao = ttk.Entry(self.frame_campos)

        self.entry_descricao.grid(
            row=0,
            column=1,
            padx=5,
            pady=5,
            sticky="ew"
        )

        if self.vulnerabilidade.descricao:
            self.entry_descricao.insert (0, self.vulnerabilidade.descricao)

        self.entry_descricao.bind(
            "<KeyRelease>",
            self.atualizar_descricao
        )

        self.frame_campos.columnconfigure(1, weight=1)

    def criar_campo_tipo(self):

        self.label_tipo = ttk.Label(
            self.frame_campos,
            text="Tipo:"
        )

        self.label_tipo.grid(
            row=1,
            column=0,
            padx=5,
            pady=5,
            sticky="w"
        )

        self.tipo_var = tk.StringVar(
            value=self.vulnerabilidade.tipo or TIPOS_VULNERABILIDADE[0]
        )

        self.combo_tipo = ttk.Combobox(
            self.frame_campos,
            textvariable=self.tipo_var,
            values=TIPOS_VULNERABILIDADE,
            state="readonly"
        )

        self.combo_tipo.grid(
            row=1,
            column=1,
            padx=5,
            pady=5,
            sticky="ew"
        )

        self.tipo_var.trace_add(
            "write",
            self.atualizar_tipo
        )

        self.atualizar_tipo()

    def criar_campo_severidade(self):

        self.label_severidade = ttk.Label(
            self.frame_campos,
            text="Severidade:"
        )

        self.label_severidade.grid(
            row=2,
            column=0,
            padx=5,
            pady=5,
            sticky="w"
        )

        self.severidade_var = tk.StringVar(
            value=self.vulnerabilidade.severidade or SEVERIDADES[0]
        )

        self.combo_severidade = ttk.Combobox(
            self.frame_campos,
            textvariable=self.severidade_var,
            values=SEVERIDADES,
            state="readonly"
        )

        self.combo_severidade.grid(
            row=2,
            column=1,
            padx=5,
            pady=5,
            sticky="ew"
        )

        self.severidade_var.trace_add(
            "write",
            self.atualizar_severidade
        )

        self.atualizar_severidade()

    def criar_campo_status(self):

        self.label_status = ttk.Label(
            self.frame_campos,
            text="Status:"
        )

        self.label_status.grid(
            row=3,
            column=0,
            padx=5,
            pady=5,
            sticky="w"
        )

        self.status_var = tk.StringVar(
            value=self.vulnerabilidade.status or STATUS_VULNERABILIDADES[0]
        )

        self.combo_status = ttk.Combobox(
            self.frame_campos,
            textvariable=self.status_var,
            values=STATUS_VULNERABILIDADES,
            state="readonly"
        )

        self.combo_status.grid(
            row=3,
            column=1,
            padx=5,
            pady=5,
            sticky="ew"
        )

        self.status_var.trace_add(
            "write",
            self.atualizar_status
        )

        self.atualizar_status()

    def criar_botoes(self):

        self.botao_excluir = ttk.Button(
            self.frame_botoes,
            text="Excluir Vulnerabilidade",
            command=self.excluir
        )

        self.botao_excluir.pack(
            side="right",
            padx=5
        )

    def excluir(self):

        self.on_remover(self.vulnerabilidade)

    def atualizar_descricao(self, event=None):

        self.vulnerabilidade.descricao = self.entry_descricao.get()

        if self.on_mudanca:
            self.on_mudanca()

    def atualizar_tipo(self, *args):

        self.vulnerabilidade.tipo = self.tipo_var.get()

        if self.on_mudanca:
            self.on_mudanca()

    def atualizar_severidade(self, *args):

        self.vulnerabilidade.severidade = self.severidade_var.get()

        self.label_titulo.config(
            fg=CORES_SEVERIDADE[self.vulnerabilidade.severidade]
        )

        if self.on_mudanca:
            self.on_mudanca()

    def atualizar_status(self, *args):

        self.vulnerabilidade.status = self.status_var.get()

        if self.on_mudanca:
            self.on_mudanca()