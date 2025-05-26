class AtividadeNotFound(Exception):
    pass

atividades = []

def listar_atividades():
    return atividades

def obter_atividade(id_atividade: int):
    for atv in atividades:
        if atv['id_atividade'] == id_atividade:
            return atv
    raise AtividadeNotFound(f"Atividade {id_atividade} não encontrada")

def criar_atividade(dados: dict):
    """
    Espera pelo menos:
      - id_atividade: int
      - id_professor: int
      - enunciado: str
    """
    atividades.append(dados)
    return dados