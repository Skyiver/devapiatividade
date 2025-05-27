from models.atividade import Atividade
from config import db
from clients.pessoa_service_client import PessoaServiceClient
from sqlalchemy.exc import IntegrityError

class AtividadeNotFound(Exception):
    pass

class AtividadeService:
    @staticmethod
    def listar_resumos():
        rows = Atividade.query.all()
        return [
            {
                'id_atividade': a.id_atividade,
                'id_professor': a.id_professor,
                'enunciado':     a.enunciado
            }
            for a in rows
        ]

    @staticmethod
    def criar(data: dict):
        # valida campos
        for campo in ('id_atividade','id_professor','enunciado'):
            if campo not in data:
                raise ValueError(f"campo {campo} obrigatório")
        # verifica professor na outra API
        if not PessoaServiceClient.existe_professor(data['id_professor']):
            raise LookupError("professor nao encontrado")

        atv = Atividade(
            id_atividade=data['id_atividade'],
            id_professor=data['id_professor'],
            enunciado=data['enunciado'],
            respostas=data.get('respostas', [])
        )
        db.session.add(atv)
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            raise ValueError("id_atividade ja existe")
        return atv.to_dict()

    @staticmethod
    def obter_completo(id_atividade: int):
        atv = Atividade.query.get(id_atividade)
        if not atv:
            raise AtividadeNotFound(f"Atividade {id_atividade} não encontrada")
        return atv.to_dict()

    @staticmethod
    def obter_para_professor(id_atividade: int, id_professor: int):
        # garante que professor existe
        if not PessoaServiceClient.existe_professor(id_professor):
            raise LookupError("professor nao encontrado")
        atv = Atividade.query.get(id_atividade)
        if not atv:
            raise AtividadeNotFound(f"Atividade {id_atividade} não encontrada")
        if atv.id_professor != id_professor:
            return {
                'id_atividade': atv.id_atividade,
                'id_professor': atv.id_professor,
                'enunciado':     atv.enunciado
            }
        return atv.to_dict()