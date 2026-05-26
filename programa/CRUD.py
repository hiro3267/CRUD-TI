import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog
import json

autosave_path = "ativos_backup.json"
autosave_job = None

# DADOS

ativos = []
ids_existentes = set()

# JANELA

janela = tk.Tk()
janela.title("Ativos")
janela.geometry("600x700")

# SCROLL

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

# CATEGORIAS

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

# CONTROLE

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

# filtro
filtro_job = None

def filtrar_ativos(event=None):

    termo = entrada_busca.get().lower().strip()

    if termo == placeholder_busca:
        termo = ''

    for categoria in categorias:

        frame_categoria = frames_categorias[categoria]

        possui_visiveis = False

        ativos_categoria = [
            ativo for ativo in ativos
            if ativo["categoria"] == categoria
            and ativo["frame"].winfo_exists()
        ]

        ativos_categoria.sort(
            key=lambda a: a["numero"]
        )

        for ativo in ativos_categoria:

            identificador = ativo["id"].lower()

            hostname = ativo["hostname"].get().lower()

            responsavel = ativo["responsavel"].get().lower()

            setor = ativo["setor"].get().lower()

            encontrou = (
                termo in identificador
                or termo in hostname
                or termo in responsavel
                or termo in setor
            )

            ativo["frame"].pack_forget()

            if encontrou or termo == '':

                ativo["frame"].pack(
                    fill='x',
                    pady=3
                )

                possui_visiveis = True

        if possui_visiveis:

            if not frame_categoria.winfo_ismapped():

                frame_categoria.pack(
                    fill='x',
                    padx=10,
                    pady=5
                )

        else:

            frame_categoria.pack_forget()

# debounce filtro
filtro_job = None

def agendar_filtro(event=None):

    global filtro_job

    if filtro_job is not None:
        janela.after_cancel(filtro_job)

    filtro_job = janela.after(
        300,
        filtrar_ativos
    )

# busca

frame_busca = tk.Frame(janela)

frame_busca.pack(
    fill='x',
    padx=10,
    pady=(0, 10)
)

entrada_busca = tk.Entry(
    frame_busca,
    fg='grey'
)

entrada_busca.pack(
    fill='x',
    expand=True
)

placeholder_busca = 'buscar ativo...'

entrada_busca.insert(0, placeholder_busca)

# placeholder de busca
def entrar_busca(event):
    if entrada_busca.get() == placeholder_busca:
        entrada_busca.delete(0, tk.END)
        entrada_busca.config(fg='black')
        entrada_busca.icursor(tk.END)

def sair_busca(event):
    if entrada_busca.get() == '':
        entrada_busca.insert(0, placeholder_busca)
        entrada_busca.config(fg='grey')
        filtrar_ativos()

entrada_busca.bind('<FocusIn>', entrar_busca)
entrada_busca.bind('<FocusOut>', sair_busca)

entrada_busca.bind('<KeyRelease>', agendar_filtro)

# placeholder da entrada
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

# NUMERAÇÃO
def renumerar_categoria(categoria):

    contador = 1

    for child in frames_categorias[categoria].winfo_children():

        if isinstance(child, tk.Frame):

            for ativo in ativos:

                if ativo["frame"] == child:

                    ativo["numero"] = contador

                    texto_id = ativo["id"]

                    cor_atual = ativo["botao"].cget('fg')

                    ativo["botao"].config(
                        text=f'● {contador}. {texto_id}',
                        fg=cor_atual
                    )

                    contador += 1
                    break

# Ordenação Numérica
def ordenar_categoria(categoria):

    ativos_categoria = [
        ativo for ativo in ativos
        if ativo["categoria"] == categoria
        and ativo["frame"].winfo_exists()
    ]

    ativos_categoria.sort(
        key=lambda a: a["numero"]
    )

    for ativo in ativos_categoria:

        ativo["frame"].pack_forget()

        ativo["frame"].pack(
            fill='x',
            pady=3
        )

    renumerar_categoria(categoria)

# ADICIONAR ITEM

def adicionar_item(event=None, carregando=False):

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

    numero = sum(
        1
        for child in frames_categorias[categoria].winfo_children()
        if isinstance(child, tk.Frame)
    ) + 1

    # FRAME ITEM

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

        if ativo_data in ativos:
            ativos.remove(ativo_data)

        item_frame.destroy()

        renumerar_categoria(categoria)

        filtrar_ativos()

        agendar_autosave()

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

    # DETALHES

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

        entry.bind(
            '<KeyRelease>',
            lambda e: (
                agendar_autosave(),
                agendar_filtro()
            )
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

    # --------------informações extras--------------

    # identificador único
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

    # VULNERABILIDADES

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

    #data ativos
    ativo_data = {
        "numero": numero,
        "id": texto,
        "categoria": categoria,
        "hostname": entry_host,
        "responsavel": entry_resp,
        "setor": entry_setor,
        "vulnerabilidades": vulnerabilidades_ativo,
        "frame": item_frame,
        "botao": botao_item,
        "visivel": True
    }

    # atualizar indicador ativo
    def atualizar_indicador():

        if not vulnerabilidades_ativo:

            botao_item.config(
                text=f'● {ativo_data["numero"]}. {texto}',
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
            text=f'● {ativo_data["numero"]}. {texto}',
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

            vulnerabilidades_ativo.remove(vulnerabilidade)

            vul_frame.destroy()

            renumerar_vulnerabilidades()

            atualizar_indicador()

            agendar_autosave()

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

        # atualizar indicador
        def ao_mudar_status(event=None):

            atualizar_indicador()

            agendar_autosave()

        combo_status.bind(
            '<<ComboboxSelected>>',
            ao_mudar_status
        )

        # cor severidade
        def atualizar_cor(event=None):

            severidade = combo_sev.get()

            cores = {
                'Baixa': 'green',
                'Média': 'orange',
                'Alta': 'red',
                'Crítica': 'purple'
            }

            cor = cores.get(
                severidade,
                'black'
            )

            botao_vul.config(
                fg=cor
            )

        def ao_mudar_severidade(event=None):

            atualizar_cor()

            agendar_autosave()

        combo_sev.bind(
            '<<ComboboxSelected>>',
            ao_mudar_severidade
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

        # data vulnerabilidade
        vulnerabilidade = {
            "descricao": entry_desc,
            "tipo": combo_tipo,
            "severidade": combo_sev,
            "status": combo_status
        }

        vulnerabilidades_ativo.append(vulnerabilidade)

        vulnerabilidade["atualizar_cor"] = atualizar_cor
        vulnerabilidade["atualizar_indicador"] = atualizar_indicador

        atualizar_cor()

        agendar_autosave()

    # renumerar vulnerabilidades
    def renumerar_vulnerabilidades():

        contador = 1

        for child in lista_vul.winfo_children():

            topo = child.winfo_children()[0]

            for widget in topo.winfo_children():

                if isinstance(widget, tk.Button):

                    texto = widget.cget("text")

                    if texto.startswith("Vulnerabilidade"):

                        widget.config(
                            text=f"Vulnerabilidade {contador}"
                        )

                        contador += 1
                        break

    # botão adicionar vulnerabilidade
    botao_add_vul = tk.Button(
        frame_vul,
        text='Adicionar Vulnerabilidade',
        cursor='hand2',
        command=adicionar_vul
    )

    ativo_data["adicionar_vul"] = adicionar_vul

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

    ativos.append(ativo_data)

    if not carregando:

        janela.after(
            10,
            filtrar_ativos
        )

    agendar_autosave()

    if not carregando:

        entrada.delete(0, tk.END)
        entrada.config(fg='black')
        entrada.focus_set()

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

entrada.bind(
    '<Return>',
    lambda event: adicionar_item()
)

# salvar
def salvar_json():

    dados = []

    for ativo in ativos:

        dados_vul = []

        for vul in ativo["vulnerabilidades"]:

            dados_vul.append({
                "descricao": vul["descricao"].get(),
                "tipo": vul["tipo"].get(),
                "severidade": vul["severidade"].get(),
                "status": vul["status"].get()
            })

        dados.append({
            "id": ativo["id"],
            "categoria": ativo["categoria"],
            "hostname": ativo["hostname"].get(),
            "responsavel": ativo["responsavel"].get(),
            "setor": ativo["setor"].get(),
            "vulnerabilidades": dados_vul
        })

    caminho = filedialog.asksaveasfilename(
        defaultextension=".json",
        filetypes=[("JSON files", "*.json")]
    )

    if not caminho:
        return

    with open(caminho, "w", encoding="utf-8") as f:
        json.dump(dados, f, indent=4, ensure_ascii=False)

    messagebox.showinfo("Sucesso", "Arquivo salvo!")

# botão de salvamento
botao_salvar = tk.Button(
    frame_controle,
    text="Salvar JSON",
    command=salvar_json
)

botao_salvar.pack(side='left', padx=10)

# salvamento automático
def salvar_auto():

    dados = []

    for ativo in ativos:

        dados_vul = []

        for vul in ativo["vulnerabilidades"]:

            dados_vul.append({
                "descricao": vul["descricao"].get(),
                "tipo": vul["tipo"].get(),
                "severidade": vul["severidade"].get(),
                "status": vul["status"].get()
            })

        dados.append({
            "id": ativo["id"],
            "categoria": ativo["categoria"],
            "hostname": ativo["hostname"].get(),
            "responsavel": ativo["responsavel"].get(),
            "setor": ativo["setor"].get(),
            "vulnerabilidades": dados_vul
        })

    with open(autosave_path, "w", encoding="utf-8") as f:
        json.dump(dados, f, indent=4, ensure_ascii=False)

# debounce
def agendar_autosave():

    global autosave_job

    if autosave_job is not None:
        janela.after_cancel(autosave_job)

    autosave_job = janela.after(2000, salvar_auto)

# carregar json
def carregar_auto():

    try:

        with open(autosave_path, "r", encoding="utf-8") as f:

            dados = json.load(f)

    except FileNotFoundError:

        return

    except json.JSONDecodeError:

        messagebox.showwarning(
            "Erro",
            "Arquivo de backup corrompido."
        )

        return

    for item in dados:

        # preencher entrada
        entrada.delete(0, tk.END)
        entrada.insert(0, item["id"])

        # selecionar categoria
        categoria_var.set(item["categoria"])

        # criar ativo
        adicionar_item(carregando=True)

        # pegar último ativo criado
        ativo = ativos[-1]

        # preencher campos
        ativo["hostname"].insert(0, item["hostname"])
        ativo["responsavel"].insert(0, item["responsavel"])
        ativo["setor"].insert(0, item["setor"])

        # recriar vulnerabilidades
        for vul in item["vulnerabilidades"]:

            ativo["adicionar_vul"]()
            nova_vul = ativo["vulnerabilidades"][-1]
            nova_vul["descricao"].insert(0, vul["descricao"])
            nova_vul["tipo"].set(vul["tipo"])
            nova_vul["severidade"].set(vul["severidade"])
            nova_vul["status"].set(vul["status"])

            nova_vul["atualizar_cor"]()
            nova_vul["atualizar_indicador"]()

    janela.after(100, filtrar_ativos)

carregar_auto()

# iniciar
janela.mainloop()