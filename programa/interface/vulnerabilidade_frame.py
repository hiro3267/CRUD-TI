import tkinter as tk
from tkinter import ttk
from models.vulnerabilidade import Vulnerabilidade
from utils.constantes import (TIPOS_VULNERABILIDADE, SEVERIDADES, STATUS_VULNERABILIDADES)

class VulnerabilidadeFrame(ttk.Frame):

    def __init__(self, parent, vulnerabilidade: Vulnerabilidade):
        super().__init__(parent)

        self.vulnerabilidade = vulnerabilidade

        self.container = ttk.LabelFrame(
            self,
            text="Vulnerabilidade"
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
            stick="ew"
        )

        self.entry_descricao = ttk.Entry(self.frame_campos)

        self.entry_descricao.grid(
            row=0,
            column=1,
            padx=5,
            pady=5,
            stick="ew"
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
            stick="w"
        )

        self.tipo_var = ttk.StringVar(
            value=TIPOS_VULNERABILIDADE[0]
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
            stick="ew"
        )

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
            stick="w"
        )

        self.severidade_var = ttk.StringVar(
            value=SEVERIDADES[0]
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
            stick="ew"
        )

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
            stick="w"
        )

        self.status_var = ttk.StringVar(
            value=STATUS_VULNERABILIDADES[0]
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
            stick="ew"
        )

    def criar_botoes(self):

        self.botao_excluir = ttk.Button(
            self.frame_botoes,
            text="Excluir Vulnerabilidade"
        )

        self.botao_excluir.pack(
            side="right",
            padx=5
        )
