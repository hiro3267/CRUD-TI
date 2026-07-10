import re

class FiltroService:
    
    def chave_ordenação(identificador):

        return [
            int(parte) if parte.isdigit() else parte.lower()
            for parte in re.split(r"(\d+)", identificador)
        ]
    
    def ordenar_ativos(cls, ativos):

        return sorted(
            ativos,
            key=lambda ativo: cls.chave_ordenação(ativo.identificador)
        )
    
    def corresponde_busca(ativo, termo):

        campos = [
            ativo.identificador,
            ativo.hostname,
            ativo.responsavel,
            ativo.setor
        ]

        return any(
            termo in campo.lower()
            for campo in campos
        )
    
    def corresponde_categoria(ativo, categoria_filtro):

        return(
            categoria_filtro == "Todas"
            or ativo.categoria == categoria_filtro
        )
    
    def corresponde(cls, ativo, termo, categoria_filtro):

        termo = termo.strip().lower()

        return(
            cls.corresponde_busca(ativo, termo)
            and cls.corresponde_categoria(ativo, categoria_filtro)
        )
    
    def filtrar_categoria(cls, ativos, categoria, termo, categoria_filtro):
        ativos_categoria = [
            ativo for ativo in ativos
            if ativo.categoria == categoria
        ]

        ativos_categoria = cls.ordenar_ativos(ativos_categoria)

        return[
            (ativo, cls.corresponde(ativo, termo, categoria_filtro))
            for ativo in ativos_categoria
        ]