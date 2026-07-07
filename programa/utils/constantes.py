#Categorias dos Ativos
CATEGORIAS = [
    "Notebook",
    "Servidor",
    "Roteador",
    "Banco de Dados",
    "Impressora"
]

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

#Placeholders
PLACEHOLDER_ID = "Identificador Único"
PLACEHOLDER_BUSCA = "Buscar Ativo..."

#Backup
AUTOSAVE_PATH = "data/ativos_backup.json"