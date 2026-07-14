import json
import os

from models.ativo import Ativo
from utils.constantes import AUTOSAVE_PATH

class AtivoRepository:

    @staticmethod
    def salvar(ativos):

        pasta = os.path.dirname(AUTOSAVE_PATH)

        if pasta:
            os.makedirs(pasta, exist_ok=True)

        dados = [ativo.to_dict() for ativo in ativos]

        with open(AUTOSAVE_PATH, "w", encoding="utf-8") as arquivo:
            json.dump(dados, arquivo, ensure_ascii=False, indent=2)

    @staticmethod
    def carregar():

        if not os.path.exists(AUTOSAVE_PATH):
            return[]
        
        try:
            with open(AUTOSAVE_PATH, "r", encoding="utf-8") as arquivo:
                dados = json.load(arquivo)

        except (json.JSONDecodeError, OSError):
            return[]
        
        return [Ativo.from_dict(item) for item in dados]

    @staticmethod
    def exportar(ativos, caminho):

        pasta = os.path.dirname(caminho)

        if pasta:
            os.makedirs(pasta, exist_ok=True)

        dados = [ativo.to_dict() for ativo in ativos]

        with open(caminho, "w", encoding="utf-8") as arquivo:
            json.dump(dados, arquivo, ensure_ascii=False, indent=2)

    @staticmethod
    def importar(caminho):

        if not os.path.exists(caminho):
            return[]
        
        try:
            with open(caminho, "r", encoding="utf-8") as arquivo:
                dados = json.load(arquivo)

        except (json.JSONDecodeError, OSError):
            return[]
        
        return [Ativo.from_dict(item) for item in dados]