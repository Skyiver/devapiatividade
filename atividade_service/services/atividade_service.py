from atividade_service.models.atividade import Atividade
from atividade_service.config import db
from atividade_service.services.pessoa_service_client import PessoaServiceClient
from sqlalchemy.exc import IntegrityError

class AtividadeNotFound(Exception):
    pass

class AtividadeService:
    @staticmethod
    def listar_resumos():
        # Corrigido: usando query moderna
        atividades = db.session.query(Atividade).all()
        return [{
            'id_atividade': a.id_atividade,
            'id_professor': a.id_professor,
            'enunciado': a.enunciado
        } for a in atividades]

    @staticmethod
    def criar(data: dict):
        campos_obrigatorios = ['id_professor', 'enunciado']
        for campo in campos_obrigatorios:
            if campo not in data:
                raise ValueError(f"Campo obrigatório faltando: {campo}")
                
        if not PessoaServiceClient.existe_professor(data['id_professor']):
            raise LookupError("Professor não encontrado")

        # Gerar ID automaticamente se não fornecido
        id_atividade = data.get('id_atividade')
        if not id_atividade:
            ultima_atividade = db.session.query(Atividade).order_by(Atividade.id_atividade.desc()).first()
            id_atividade = ultima_atividade.id_atividade + 1 if ultima_atividade else 1

        nova_atividade = Atividade(
            id_atividade=id_atividade,
            id_professor=data['id_professor'],
            enunciado=data['enunciado'],
            respostas=data.get('respostas', [])
        )
        
        db.session.add(nova_atividade)
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            raise ValueError("ID da atividade já existe")
            
        return nova_atividade.to_dict()

    @staticmethod
    def obter_completo(id_atividade: int):
        # Corrigido: usando Session.get() moderno
        atividade = db.session.get(Atividade, id_atividade)
        if not atividade:
            raise AtividadeNotFound(f"Atividade {id_atividade} não encontrada")
        return atividade.to_dict()

    @staticmethod
    def obter_para_professor(id_atividade: int, id_professor: int):
        if not PessoaServiceClient.existe_professor(id_professor):
            raise LookupError("Professor não encontrado")
            
        # Corrigido: usando Session.get() moderno
        atividade = db.session.get(Atividade, id_atividade)
        if not atividade:
            raise AtividadeNotFound(f"Atividade {id_atividade} não encontrada")
            
        if atividade.id_professor != id_professor:
            return {
                'id_atividade': atividade.id_atividade,
                'id_professor': atividade.id_professor,
                'enunciado': atividade.enunciado
            }
            
        return atividade.to_dict()