from atividade_service.config import db

class Atividade(db.Model):
    __tablename__ = 'atividades'
    
    id_atividade = db.Column(db.Integer, primary_key=True)
    id_professor = db.Column(db.Integer, nullable=False)
    enunciado = db.Column(db.Text, nullable=False)
    respostas = db.Column(db.JSON, nullable=False, default=[])

    def to_dict(self):
        return {
            'id_atividade': self.id_atividade,
            'id_professor': self.id_professor,
            'enunciado': self.enunciado,
            'respostas': self.respostas
        }