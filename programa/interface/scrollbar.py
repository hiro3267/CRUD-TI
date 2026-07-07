import tkinter as tk
import platform

class ScrollbarFrame(tk.Frame):

    def __init__(self, parent):
        super().__init__(parent)

        self.canvas = tk.Canvas(
            self,
            highlightthickness=0
        )

        self.scrollbar = tk.Scrollbar(
            self,
            orient="vertical",
            command=self.canvas.yview
        )

        self.canvas.configure(
            yscrollcommand=self.scrollbar.set
        )

        self.scrollbar.pack(
            side="right",
            fill="y"
        )

        self.canvas.pack(
            side="left",
            fill="both",
            expand=True
        )

        self.content = tk.Frame(self.canvas)

        self.window = self.canvas.create_window(
            (0 , 0),
            window=self.content,
            anchor="nw"
        )

        self.content.bind(
            "<Configure>",
            self._atualizar_scroll
        )

        self.canvas.bind(
            "<Configure>",
            self._ajustar_largura
        )

        self._config_scroll_mouse()

    def _atualizar_scroll(self, event=None):

        self.canvas.configure(
            scrollregion=self.canvas.bbox("all")
        )

    def _ajustar_largura(self, event):

        self.canvas.itemconfigure(
            self.window,
            width=event.width
        )

    def _rolar_mouse(self, event):

        if event.delta:

            self.canvas.yview_scroll(
                int(-event.delta / 120),
                "units"
            )
        elif event.num == 4:

            self.canvas.yview_scroll(
                -1,
                "units"
            )

        elif event.num == 5:

            self.canvas.yview_scroll(
                1,
                "units"
            )

    def _config_scroll_mouse(self):

        sistema = platform.system()

        if sistema == "Linux":

            self.canvas.bind_all(
                "<Button-4>",
                self._rolar_mouse
            )

            self.canvas.bind_all(
                "<Button-5>",
                self._rolar_mouse
            )