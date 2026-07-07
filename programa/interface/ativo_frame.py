from tkinter import ttk
from models.ativo import Ativo

class AtivoFrame(ttk.Frame):

    def __init__(self, parent, ativo: Ativo):
        super().__init__(parent)

        self.ativo = ativo

        self.container = ttk.LabelFrame(
            self,
            text=f"Ativo: {ativo.identificador}"
        )

        self.container.pack(
            fill="x",
            expand=True
        )

        self.criar_widgets()

    def criar_widgets(self):

        self.criar_frame_campos()
        self.criar_frame_vulnerabilidades()
        self.criar_frame_botoes()

    def criar_frame_campos(self):

        self.frame_campos = ttk.Frame(self.container)

        self.frame_campos.pack(
            fill="x",
            padx=10,
            pady=10
        )