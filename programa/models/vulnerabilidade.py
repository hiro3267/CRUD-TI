class Vulnerabilidade:

    def __init__(
            self,
            descricao="",
            tipo="",
            severidade="",
            status="",
    ):
        self.descricao = descricao
        self.tipo = tipo
        self.severidade = severidade
        self.status = status