from models.vulnerabilidade import Vulnerabilidade

class Ativo:

    def __init__(
            self,
            identificador,
            categoria,
            hostname = "",
            responsavel = "",
            setor = "",
            vulnerabilidades = None
    ):
        self.identificador = identificador
        self.categoria = categoria

        self.hostname = hostname
        self.responsavel = responsavel
        self.setor = setor

        self.vulnerabilidades = vulnerabilidades if vulnerabilidades is not None else[]

    def to_dict(self):

        return {
            "identificador": self.identificador,
            "categoria": self.categoria,
            "hostname": self.hostname,
            "responsavel": self.responsavel,
            "setor": self.setor,
            "vulnerabilidades": [
                Vulnerabilidade.to_dict()
                for vulnerabilidade in self.vulnerabilidades
            ]
        }
    
    @classmethod
    def from_dict(cls, dados):

        ativo = cls(
            identificador=dados["identificador"],
            categoria=dados["categoria"],
            hostname=dados.get("hostname", ""),
            responsavel=dados.get("responsavel", ""),
            setor=dados.get("setor", "")
        )

        ativo.vulnerabilidades = [
            Vulnerabilidade.from_dict(item)
            for item in dados.get("vulnerabilidades", [])
        ]

        return ativo