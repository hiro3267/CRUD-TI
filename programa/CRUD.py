import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import json

ativos = []

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

ids_existentes = set()

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
    fg='black'
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

    if texto in ids_existentes:
        messagebox.showwarning(
            'Duplicado',
            'Esse identificador já existe.'
        )
        return
    
    ids_existentes.add(texto)

    if not frames_categorias[categoria].winfo_ismapped():
        frames_categorias[categoria].pack(
            fill='x',
            padx=10,
            pady=5
        )

    numero = len(
        frames_categorias[categoria].pack_slaves()
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

    # botão excluir
    def excluir_item():
        ids_existentes.remove(texto)

        item_frame.destroy()

        if not frames_categorias[categoria].winfo_children():

            frames_categorias[categoria].pack_forget()

    botao_excluir = tk.Button(
        item_frame,
        text='Excluir',
        fg='white',
        bg='red',
        cursor='hand2',
        command=excluir_item
    )

    botao_excluir.pack(anchor='e', padx=5, pady=2)

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
    frame_vul = tk.LabelFrame(
        detalhes,
        text='Vulnerabilidades',
        padx=5,
        pady=5
    )
    frame_vul.pack(fill='x', pady=5)

    lista_vul = tk.Frame(frame_vul)
    lista_vul.pack(fill='x')

    # adicionar vulnerabilidade
    def adicionar_vul():
        numero_vul = len(
            lista_vul.winfo_children()
        ) + 1

        vul_frame = tk.Frame(
            lista_vul,
            bd=1,
            relief='solid'
        )

        vul_frame.pack(fill='x', pady=3)

        # topo
        topo_vul = tk.Frame(vul_frame)
        topo_vul.pack(fill='x')

        botao_vul = tk.Button(
            topo_vul,
            text=f'Vulnerabilidade {numero_vul}',
            relief='flat',
            anchor='w'
        )

        botao_vul.pack(
            side='left',
            fill='x',
            expand=True
        )

    # excluir vulnerabilidade
        def excluir_vul():
            vul_frame.destroy()

        botao_excluir_vul = tk.Button(
            topo_vul,
            text='x',
            bg='red',
            fg='white',
            width=3,
            command=excluir_vul,
            cursor='hand2'
        )

        botao_excluir_vul.pack(side='right')

        # detalhes vulnerabilidade
        detalhes_vul = tk.Frame(vul_frame)

        # descrição
        frame_desc = tk.Frame(detalhes_vul)
        frame_desc.pack(fill='x', pady=2)

        tk.Label(
            frame_desc,
            text='Descrição:',
            width=15,
            anchor='w'
        ).pack(side='left')

        entry_desc = tk.Entry(frame_desc)

        entry_desc.pack(
            side='left',
            fill='x',
            expand=True
        )

        # tipo
        frame_tipo = tk.Frame(detalhes_vul)
        frame_tipo.pack(fill='x', pady=2)

        tk.Label(
            frame_tipo,
            text='Tipo:',
            width=15,
            anchor='w'
        ).pack(side='left')

        combo_tipo = ttk.Combobox(
            frame_tipo,
            values=[
                'Software',
                'Hardware',
                'Rede',
                'Configuração'
            ],
            state='readonly'
        )

        combo_tipo.pack(
            side='left',
            fill='x',
            expand=True
        )

        # severidade
        frame_sev = tk.Frame(detalhes_vul)
        frame_sev.pack(fill='x', pady=2)

        tk.Label(
            frame_sev,
            text='Severidade:',
            width=15,
            anchor='w'
        ).pack(side='left')

        combo_sev = ttk.Combobox(
            frame_sev,
            values=[
                'Baixa',
                'Média',
                'Alta',
                'Crítica'
            ],
            state='readonly'
        )

        combo_sev.pack(
            side='left',
            fill='x',
            expand=True
        )

        # status
        frame_status = tk.Frame(detalhes_vul)
        frame_status.pack(fill='x', pady=2)

        tk.Label(
            frame_status,
            text='Status:',
            width=15,
            anchor='w'
        ).pack(side='left')

        combo_status = ttk.Combobox(
            frame_status,
            values=[
                'Aberta',
                'Em tratamento',
                'Corrigida',
                'Aceita'
            ],
            state='readonly'
        )

        combo_status.pack(
            side='left',
            fill='x',
            expand=True
        )

        # expandir/recolher
        visivel = False

        def alternar_vul():

            nonlocal visivel

            if visivel:
                detalhes_vul.pack_forget()
            else:
                detalhes_vul.pack(
                    fill='x',
                    padx=10,
                    pady=5
                )

            visivel = not visivel

        botao_vul.config(command=alternar_vul)

    # botão adicionar vulnerabilidade
    botao_add_vul = tk.Button(
        frame_vul,
        text='Adicionar Vulnerabilidade',
        command=adicionar_vul,
        cursor='hand2'
    )

    botao_add_vul.pack(
        fill='x',
        pady=5
    )

    # Dicionário
    ativo = {
        'id': texto,
        'categoria': categoria,
        'hostname': entry_host.get(),
        'responsável': entry_resp.get(),
        'setor': entry_setor.get(),
        'vulnerabilidades': []
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