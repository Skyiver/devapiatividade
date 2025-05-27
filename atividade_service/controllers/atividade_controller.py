from flask import Blueprint, jsonify, request
from services.atividade_service import (
    AtividadeService, AtividadeNotFound
)

atividade_bp = Blueprint('atividade_bp', __name__)

@atividade_bp.route('/', methods=['GET'])
def get_atividades():
    return jsonify(AtividadeService.listar_resumos()), 200

@atividade_bp.route('/', methods=['POST'])
def post_atividade():
    try:
        novo = AtividadeService.criar(request.get_json() or {})
        return jsonify(novo), 201
    except ValueError as e:
        return jsonify({"erro": str(e)}), 400
    except LookupError as e:
        return jsonify({"erro": str(e)}), 404

@atividade_bp.route('/<int:id_atividade>', methods=['GET'])
def get_atividade(id_atividade):
    try:
        return jsonify(AtividadeService.obter_completo(id_atividade)), 200
    except AtividadeNotFound as e:
        return jsonify({'erro': str(e)}), 404

@atividade_bp.route(
    '/<int:id_atividade>/professor/<int:id_professor>',
    methods=['GET']
)
def get_atividade_para_professor(id_atividade, id_professor):
    try:
        result = AtividadeService.obter_para_professor(
            id_atividade, id_professor
        )
        return jsonify(result), 200
    except LookupError as e:
        return jsonify({"erro": str(e)}), 404
    except AtividadeNotFound as e:
        return jsonify({'erro': str(e)}), 404