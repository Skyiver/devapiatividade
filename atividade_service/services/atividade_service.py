from models.atividade_model import (
    listar_atividades, obter_atividade, criar_atividade, AtividadeNotFound
)
from clients.pessoa_service_client import PessoaServiceClient

class AtividadeService:
    @staticmethod
    def listar_resumos():
        # devolve somente os campos de resumo
        return [
            {
                'id_atividade': atv['id_atividade'],
                'id_professor': atv['id_professor'],
                'enunciado': atv['enunciado']
            }
            for atv in listar_atividades()
        ]

    @staticmethod
    def criar(dados: dict):
        # valida campos obrigatórios
        if not all(k in dados for k in ('id_atividade','id_professor','enunciado')):
            raise ValueError("campos id_atividade, id_professor e enunciado são obrigatórios")
        # verifica que professor realmente existe
        if not PessoaServiceClient.existe_professor(dados['id_professor']):
            raise LookupError("professor nao encontrado")
        return criar_atividade(dados)

    @staticmethod
    def obter_completo(id_atividade: int):
        return obter_atividade(id_atividade)

    @staticmethod
    def obter_para_professor(id_atividade: int, id_professor: int):
        atv = obter_atividade(id_atividade)
        # se professor diferente, omitimos respostas
        if atv['id_professor'] != id_professor:
            return {
                'id_atividade': atv['id_atividade'],
                'id_professor': atv['id_professor'],
                'enunciado': atv['enunciado']
            }
        return atv