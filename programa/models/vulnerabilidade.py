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

    def to_dict(self):

        return {
            "descricao": self.descricao,
            "tipo": self.tipo,
            "severidade": self.severidade,
            "status": self.status
        }
    
    @classmethod
    def from_dict(cls, dados):

        return cls(
            descricao=dados.get("descricao", ""),
            tipo=dados.get("tipo", ""),
            severidade=dados.get("severidade", ""),
            status=dados.get("status", "")
        )