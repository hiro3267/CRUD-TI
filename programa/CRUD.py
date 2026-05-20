import tkinter as tk
from tkinter import ttk
import json

# janela
janela = tk.Tk()
janela.title("Ativos")
janela.geometry("400x600")

# área com scrollbar
container=tk.Frame(janela)
container.pack(fill='both', expand=True, padx=10, pady=10)

canvas=tk.Canvas(
    container,
    highlightthickness=0
    )

scrollbar=tk.Scrollbar(
    container,
    orient='vertical',
    command=canvas.yview
)

canvas.configure(yscrollcommand=scrollbar.set)

scrollbar.pack(side='right',fill='y')
canvas.pack(side='left', fill='both', expand=True)

frame_principal=tk.Frame(canvas)

canvas_window = canvas.create_window(
    (0,0),
    window=frame_principal,
    anchor='nw'
)

#atualizar região scroll
def atualizar_scroll(event):
    canvas.configure(
        scrollregion=canvas.bbox('all')
    )

frame_principal.bind(
    '<Configure>',
    atualizar_scroll
)

def ajustar_largura(event):
    canvas.itemconfig(
        canvas_window,
        width=event.width
    )

canvas.bind('<Configure>',ajustar_largura)

#scroll com roda do mouse
def rolar_mouse(event):
    if event.delta:
        canvas.yview_scroll(
            int(-1*(event.delta/120)),
            'units'
        )

    elif event.num == 4:
        canvas.yview_scroll(-1, 'units')
    elif event.num == 5:
        canvas.yview_scroll(1, 'units')

canvas.bind_all('<MouseWheel>', rolar_mouse)

canvas.bind_all('<Button-4>', rolar_mouse)
canvas.bind_all('<Button-5>', rolar_mouse)

# categorias
categorias = [
    'Notebook',
    'Servidor',
    'Roteador',
    'Banco de Dados',
    'Impressora de Rede',
    'Estação de Trabalho'
]

frames_categorias = {}

for idendificador in categorias:

    frame = tk.LabelFrame(
        frame_principal,
        text=idendificador,
        padx=10,
        pady=10
    )

    frame.pack(
        fill='x',
        padx=10,
        pady=5
    )

    frames_categorias[idendificador] = frame

# entrada
frame_controle = tk.Frame(janela)
frame_controle.pack(fill='x', padx=10, pady=10)

def validar(valor):

    if valor == "":
        return True
    
    return valor.isdigit()

vcmd = janela.register(validar)

entrada = tk.Entry(
    frame_controle,
    validate='key',
    validatecommand=(vcmd, '%P'),
    fg='grey'
    )

entrada.pack(side='left', fill='x', expand=True, padx=(0,10))

# placeholder
placeholder = 'identificador único'

entrada.insert(0,placeholder)

def entrar_entry(event):
    if entrada.get() == placeholder:
        entrada.delete(0, tk.END)
        entrada.configure(fg='black')

def sair_entry(event):
    if entrada.get() == '':
        entrada.insert(0, placeholder)
        entrada.config(fg='grey')

entrada.bind('<FocusIn>', entrar_entry)
entrada.bind('<FocusOut>', sair_entry)

# categoria
categoria_var = tk.StringVar()
categoria_var.set(categorias[0])

menu = ttk.Combobox(
    frame_controle,
    textvariable=categoria_var,
    values=categorias,
    state='readonly',
    width=15
)

menu.pack(side='left')

# adicionar item
def adicionar_item():
    texto = entrada.get().strip()

    if texto == "" or texto == placeholder:
        return
    
    categoria = categoria_var.get()

    numero = len(
        frames_categorias[categoria].winfo_children()
    ) + 1

    label = tk.Label(
        frames_categorias[categoria],
        text=f"{numero}. {texto}",
        anchor='w'
    )

    label.pack(fill='x', pady=2)

    entrada.delete(0, tk.END)

botao = tk.Button(
    frame_controle,
    text='Adicionar',
    command=adicionar_item
)

botao.pack(side='left', padx=(10,0))

janela.mainloop()