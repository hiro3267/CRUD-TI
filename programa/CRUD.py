import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

# =========================
# DADOS
# =========================

ativos = []
ids_existentes = set()

# =========================
# JANELA
# =========================

janela = tk.Tk()
janela.title("Ativos")
janela.geometry("500x700")

# =========================
# SCROLL
# =========================

container = tk.Frame(janela)
container.pack(fill='both', expand=True, padx=10, pady=10)

canvas = tk.Canvas(
    container,
    highlightthickness=0
)

scrollbar = tk.Scrollbar(
    container,
    orient='vertical',
    command=canvas.yview
)

canvas.configure(
    yscrollcommand=scrollbar.set
)

scrollbar.pack(side='right', fill='y')
canvas.pack(side='left', fill='both', expand=True)

frame_principal = tk.Frame(canvas)

canvas_window = canvas.create_window(
    (0, 0),
    window=frame_principal,
    anchor='nw'
)

# atualizar scroll
def atualizar_scroll(event):

    canvas.configure(
        scrollregion=canvas.bbox('all')
    )

frame_principal.bind(
    '<Configure>',
    atualizar_scroll
)

# ajustar largura
def ajustar_largura(event):

    canvas.itemconfig(
        canvas_window,
        width=event.width
    )

canvas.bind(
    '<Configure>',
    ajustar_largura
)

# rolagem mouse
def rolar_mouse(event):

    if event.delta:

        canvas.yview_scroll(
            int(-1 * (event.delta / 120)),
            'units'
        )

    elif event.num == 4:

        canvas.yview_scroll(-1, 'units')

    elif event.num == 5:

        canvas.yview_scroll(1, 'units')

canvas.bind_all('<MouseWheel>', rolar_mouse)
canvas.bind_all('<Button-4>', rolar_mouse)
canvas.bind_all('<Button-5>', rolar_mouse)

# =========================
# CATEGORIAS
# =========================

categorias = [
    'Notebook',
    'Servidor',
    'Roteador',
    'Banco de Dados',
    'Impressora de Rede',
    'Estação de Trabalho'
]

frames_categorias = {}

for categoria in categorias:

    frame = tk.LabelFrame(
        frame_principal,
        text=categoria,
        padx=10,
        pady=10
    )

    frame.pack(
        fill='x',
        padx=10,
        pady=5
    )

    frames_categorias[categoria] = frame

# =========================
# CONTROLE
# =========================

frame_controle = tk.Frame(janela)

frame_controle.pack(
    fill='x',
    padx=10,
    pady=10
)

entrada = tk.Entry(
    frame_controle,
    fg='grey'
)

entrada.pack(
    side='left',
    fill='x',
    expand=True,
    padx=(0, 10)
)

placeholder = 'identificador único'

entrada.insert(0, placeholder)

# placeholder
def entrar_entry(event):

    if entrada.get() == placeholder:

        entrada.delete(0, tk.END)
        entrada.config(fg='black')

def sair_entry(event):

    if entrada.get() == '':

        entrada.insert(0, placeholder)
        entrada.config(fg='grey')

entrada.bind('<FocusIn>', entrar_entry)
entrada.bind('<FocusOut>', sair_entry)

# combobox categoria
categoria_var = tk.StringVar()
categoria_var.set(categorias[0])

menu = ttk.Combobox(
    frame_controle,
    textvariable=categoria_var,
    values=categorias,
    state='readonly',
    width=18
)

menu.pack(side='left')

# =========================
# ADICIONAR ITEM
# =========================

def adicionar_item():

    texto = entrada.get().strip()

    if texto == '' or texto == placeholder:
        return

    if not texto.isdigit():

        messagebox.showwarning(
            'Inválido',
            'O identificador deve conter apenas números.'
        )

        return

    if texto in ids_existentes:

        messagebox.showwarning(
            'Duplicado',
            'Esse identificador já existe.'
        )

        return

    ids_existentes.add(texto)

    categoria = categoria_var.get()

    # reaparecer categoria
    if not frames_categorias[categoria].winfo_ismapped():

        frames_categorias[categoria].pack(
            fill='x',
            padx=10,
            pady=5
        )

    numero = len(
        frames_categorias[categoria].pack_slaves()
    ) + 1

    # =========================
    # FRAME ITEM
    # =========================

    item_frame = tk.Frame(
        frames_categorias[categoria],
        bd=1,
        relief='solid'
    )

    item_frame.pack(
        fill='x',
        pady=3
    )

    # topo item
    topo_item = tk.Frame(item_frame)
    topo_item.pack(fill='x')

    # botão principal
    botao_item = tk.Button(
        topo_item,
        text=f'● {numero}. {texto}',
        fg='green',
        anchor='w',
        relief='flat'
    )

    botao_item.pack(
        side='left',
        fill='x',
        expand=True
    )

    # excluir item
    def excluir_item():

        ids_existentes.remove(texto)

        item_frame.destroy()

        if not frames_categorias[categoria].winfo_children():

            frames_categorias[categoria].pack_forget()

    botao_excluir = tk.Button(
        topo_item,
        text='X',
        bg='red',
        fg='white',
        width=3,
        cursor='hand2',
        command=excluir_item
    )

    botao_excluir.pack(side='right')

    # =========================
    # DETALHES
    # =========================

    detalhes = tk.Frame(item_frame)

    # função criar campo
    def criar_campo(parent, nome):

        frame = tk.Frame(parent)

        frame.pack(
            fill='x',
            pady=2
        )

        tk.Label(
            frame,
            text=nome,
            width=18,
            anchor='w'
        ).pack(side='left')

        entry = tk.Entry(frame)

        entry.pack(
            side='left',
            fill='x',
            expand=True
        )

        return entry

    # ID
    frame_id = tk.Frame(detalhes)

    frame_id.pack(
        fill='x',
        pady=2
    )

    tk.Label(
        frame_id,
        text='Identificador:',
        width=18,
        anchor='w'
    ).pack(side='left')

    tk.Label(
        frame_id,
        text=texto
    ).pack(side='left')

    # campos
    entry_host = criar_campo(detalhes, 'Hostname:')
    entry_resp = criar_campo(detalhes, 'Responsável:')
    entry_setor = criar_campo(detalhes, 'Setor:')

    # tipo ativo
    frame_tipo = tk.Frame(detalhes)

    frame_tipo.pack(
        fill='x',
        pady=2
    )

    tk.Label(
        frame_tipo,
        text='Tipo:',
        width=18,
        anchor='w'
    ).pack(side='left')

    tk.Label(
        frame_tipo,
        text=categoria
    ).pack(side='left')

    # =========================
    # VULNERABILIDADES
    # =========================

    vulnerabilidades_ativo = []

    frame_vul = tk.LabelFrame(
        detalhes,
        text='Vulnerabilidades',
        padx=5,
        pady=5
    )

    frame_vul.pack(
        fill='x',
        pady=5
    )

    lista_vul = tk.Frame(frame_vul)

    lista_vul.pack(fill='x')

    # atualizar indicador ativo
    def atualizar_indicador():

        if not vulnerabilidades_ativo:

            botao_item.config(
                text=f'● {numero}. {texto}',
                fg='green'
            )
            return

        estados = [vul['status'].get() for vul in vulnerabilidades_ativo]

    # vermelho: risco
        if any(s in ('Aberta', 'Em tratamento') for s in estados):

            cor = 'red'

    # amarelo: Aceita
        elif any(s == 'Aceita' for s in estados):

            cor = 'goldenrod'

    # verde: corrigido
        else:

            cor = 'green'

        botao_item.config(
            text=f'● {numero}. {texto}',
            fg=cor
        )

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

        vul_frame.pack(
            fill='x',
            pady=3
        )

        # topo vulnerabilidade
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

            vulnerabilidades_ativo.remove(
                vulnerabilidade
            )

            vul_frame.destroy()

            atualizar_indicador()

        botao_excluir_vul = tk.Button(
            topo_vul,
            text='X',
            bg='red',
            fg='white',
            width=3,
            cursor='hand2',
            command=excluir_vul
        )

        botao_excluir_vul.pack(side='right')

        # detalhes vulnerabilidade
        detalhes_vul = tk.Frame(vul_frame)

        # descrição
        entry_desc = criar_campo(
            detalhes_vul,
            'Descrição:'
        )

        # tipo
        frame_tipo_vul = tk.Frame(detalhes_vul)

        frame_tipo_vul.pack(
            fill='x',
            pady=2
        )

        tk.Label(
            frame_tipo_vul,
            text='Tipo:',
            width=15,
            anchor='w'
        ).pack(side='left')

        combo_tipo = ttk.Combobox(
            frame_tipo_vul,
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

        frame_sev.pack(
            fill='x',
            pady=2
        )

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

        frame_status.pack(
            fill='x',
            pady=2
        )

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

        # salvar vulnerabilidade
        vulnerabilidade = {
            'frame': vul_frame,
            'status': combo_status
        }

        vulnerabilidades_ativo.append(
            vulnerabilidade
        )

        # atualizar indicador
        combo_status.bind(
            '<<ComboboxSelected>>',
            lambda e: atualizar_indicador()
        )

        # cor severidade
        def atualizar_cor(event=None):

            severidade = combo_sev.get()

            cores = {
                'Baixa': 'green',
                'Média': 'orange',
                'Alta': 'red',
                'Crítica': 'black'
            }

            cor = cores.get(
                severidade,
                'black'
            )

            botao_vul.config(
                fg=cor
            )

        combo_sev.bind(
            '<<ComboboxSelected>>',
            atualizar_cor
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

        botao_vul.config(
            command=alternar_vul
        )

        atualizar_indicador()

    # botão adicionar vulnerabilidade
    botao_add_vul = tk.Button(
        frame_vul,
        text='Adicionar Vulnerabilidade',
        cursor='hand2',
        command=adicionar_vul
    )

    botao_add_vul.pack(
        fill='x',
        pady=5
    )

    # expandir detalhes ativo
    detalhes_visivel = False

    def alternar():

        nonlocal detalhes_visivel

        if detalhes_visivel:

            detalhes.pack_forget()

        else:

            detalhes.pack(
                fill='x',
                padx=10,
                pady=5
            )

        detalhes_visivel = not detalhes_visivel

    botao_item.config(
        command=alternar
    )

# botão adicionar
botao = tk.Button(
    frame_controle,
    text='Adicionar',
    command=adicionar_item
)

botao.pack(
    side='left',
    padx=(10, 0)
)

# iniciar
janela.mainloop()