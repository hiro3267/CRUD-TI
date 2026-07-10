#Categorias dos Ativos
CATEGORIAS = [
    "Notebook",
    "Servidor",
    "Roteador",
    "Banco de Dados",
    "Impressora"
]

#Prefixos IDs
PREFIXOS_CATEGORIA = {
    "Notebook": "NB",
    "Servidor": "SV",
    "Roteador": "RT",
    "Banco de Dados": "DB",
    "Impressora": "IM"
}

#Tipos de Volnerabilidade
TIPOS_VULNERABILIDADE = [
    "Software",
    "Hardware",
    "Rede",
    "Configuração"
]

#Severidades
SEVERIDADES = [
    "Baixa",
    "Média",
    "Alta",
    "Crítica"
]

#Status
STATUS_VULNERABILIDADES = [
    "Aberta",
    "Em Tratamento",
    "Corrigida",
    "Aceita"
]

#Cores
CORES_SEVERIDADE = {
    "Baixa": "green",
    "Média": "orange",
    "Alta": "red",
    "Crítica": "purple"
}

#Cores dos status da vulnerabilidade
CORES_INDICADOR_ATIVO = {
    "risco":  "red",
    "aceita": "goldenrod",
    "ok":     "green"
}

#Placeholders
PLACEHOLDER_ID = "Identificador Único"
PLACEHOLDER_BUSCA = "Buscar Ativo..."

#Backup
AUTOSAVE_PATH = "data/ativos_backup.json"