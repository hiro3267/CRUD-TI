from models.vulnerabilidade import Vulnerabilidade

class Ativo:

    def __init__(
            self,
            identificador,
            categoria
    ):
        self.identificador = identificador
        self.categoria = categoria

        self.hostname = ""
        self.responsável = ""
        self.setor = ""

        self.vulnerabilidades = []
        