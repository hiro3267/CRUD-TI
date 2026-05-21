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

    # frame do item
    item_frame = tk.Frame(
        frames_categorias[categoria],
        bd=1,
        relief='solid'
    )

    item_frame.pack(
        fill='x',
        pady=3
    )

    # botão principal
    botao_item = tk.Button(
        item_frame,
        text=f"{numero}. {texto}",
        anchor='w',
        relief='flat'
    )

    botao_item.pack(fill='x')

    # area de detalhes
    detalhes = tk.Frame(item_frame)

    # -----------------informações extras-----------------

    # Identificador único
    frame_id = tk.Frame(detalhes)
    frame_id.pack(fill='x', pady=2)

    tk.Label(
        frame_id,
        text='Identificador Único:',
        width=18,
        anchor='w'
    ).pack(side='left')

    tk.Label(
        frame_id,
        text=texto,
        anchor='w'
    ).pack(side='left')

    # Hostname
    frame_host = tk.Frame(detalhes)
    frame_host.pack(fill='x', pady=2)

    tk.Label(
        frame_host,
        text='Hostname:',
        width=18,
        anchor='w'
    ).pack(side='left')

    entry_host = tk.Entry(frame_host)

    entry_host.pack(
        side='left',
        fill='x',
        expand=True
    )

    # Responsável
    frame_resp = tk.Frame(detalhes)
    frame_resp.pack(fill='x', pady=2)

    tk.Label(
        frame_resp,
        text='Responsável:',
        width=18,
        anchor='w'
    ).pack(side='left')

    entry_resp = tk.Entry(frame_resp)

    entry_resp.pack(
        side='left',
        fill='x',
        expand=True
    )

    # Setor
    frame_setor = tk.Frame(detalhes)
    frame_setor.pack(fill='x', pady=2)

    tk.Label(
        frame_setor,
        text='Setor:',
        width=18,
        anchor='w'
    ).pack(side='left')

    entry_setor = tk.Entry(frame_setor)

    entry_setor.pack(
        side='left',
        fill='x',
        expand=True
    )
    
    # Tipo de Ativo
    frame_ativo = tk.Frame(detalhes)
    frame_ativo.pack(fill='x', pady=2)

    tk.Label(
        frame_ativo,
        text='Tipo de ativo:',
        width=18,
        anchor='w'
    ).pack(side='left')

    tk.Label(
        frame_ativo,
        text=categoria,
        anchor='w'
    ).pack(side='left')

    # Vulnerabilidades
    frame_vul = tk.Frame(detalhes)
    frame_vul.pack(fill='x', pady=2)

    tk.Label(
        frame_vul,
        text='Vulnerabilidades:',
        width=18,
        anchor='w'
    ).pack(side='left')

    entry_vul = tk.Entry(frame_vul)

    entry_vul.pack(
        side='left',
        fill='x',
        expand=True
    )

    # Dicionário
    ativo = {
        'id': texto,
        'categoria': categoria,
        'hostname': entry_host,
        'responsável': entry_resp,
        'setor': entry_setor,
        'vulnerabilidades': entry_vul
    }

    #visibilidade dos detalhes
    detalhes_visi = False

    def alternar():
        nonlocal detalhes_visi

        if detalhes_visi:
            detalhes.pack_forget()
        else:
            detalhes.pack(
                fill='x',
                padx=10,
                pady=5
            )
        detalhes_visi = not detalhes_visi
    botao_item.config(command=alternar)

botao = tk.Button(
    frame_controle,
    text='Adicionar',
    command=adicionar_item
)

botao.pack(side='left', padx=(10,0))

janela.mainloop()