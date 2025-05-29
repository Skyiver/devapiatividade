import os
import sys
import pytest
import requests_mock
import re

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from atividade_service.app import create_app
from atividade_service.config import db
from atividade_service.controllers.atividade_controller import atividade_bp
from atividade_service.services.pessoa_service_client import PESSOA_SERVICE_URL

@pytest.fixture
def client():
    # Cria aplicação e banco em memória
    app = create_app()
    app.register_blueprint(atividade_bp, url_prefix='/api/atividades')
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    with app.app_context():
        db.create_all()
    with app.test_client() as client:
        yield client
    # Cleanup após cada teste
    with app.app_context():
        db.session.remove()
        db.drop_all()

@pytest.fixture
def mock_professor_service():
    with requests_mock.Mocker() as m:
        # Regex compatível com URL real do serviço de professores
        url_pattern = re.compile(f"{re.escape(PESSOA_SERVICE_URL)}/\\d+")
        m.get(url_pattern,
              json=lambda request, context: {
                  "id": int(request.url.split('/')[-1]),
                  "tipo": "professor"
              },
              status_code=200)
        yield m

# Testes básicos de GET e POST
def test_listar_atividades_vazio(client):
    response = client.get("/api/atividades/")
    assert response.status_code == 200
    assert response.json == []

def test_obter_atividade_nao_encontrada(client):
    response = client.get("/api/atividades/999")
    assert response.status_code == 404
    assert 'erro' in response.json
    assert 'não encontrada' in response.json['erro']

def test_criar_atividade(client, mock_professor_service):
    nova_atividade = {
        "id_professor": 101,
        "enunciado": "Desenvolver API RESTful"
    }

    response = client.post("/api/atividades/", json=nova_atividade)
    assert response.status_code == 201
    assert 'id_atividade' in response.json
    assert response.json['enunciado'] == "Desenvolver API RESTful"

def test_listar_atividades_apos_criacao(client, mock_professor_service):
    nova_atividade = {
        "id_professor": 101,
        "enunciado": "Desenvolver API RESTful"
    }
    post = client.post("/api/atividades/", json=nova_atividade)
    id_atividade = post.json['id_atividade']

    response = client.get("/api/atividades/")
    assert response.status_code == 200
    assert len(response.json) == 1
    assert response.json[0]['id_atividade'] == id_atividade

def test_obter_atividade_existente(client, mock_professor_service):
    nova = {"id_professor": 101, "enunciado": "Desenvolver API RESTful"}
    post = client.post("/api/atividades/", json=nova)
    id_atividade = post.json['id_atividade']

    response = client.get(f"/api/atividades/{id_atividade}")
    assert response.status_code == 200
    assert response.json['id_atividade'] == id_atividade
    assert response.json['enunciado'] == nova['enunciado']

def test_criar_atividade_id_duplicado(client, mock_professor_service):
    atividade = {
        "id_atividade": 1001,
        "id_professor": 101,
        "enunciado": "Primeira atividade"
    }
    resp1 = client.post("/api/atividades/", json=atividade)
    assert resp1.status_code == 201

    resp2 = client.post("/api/atividades/", json=atividade)
    assert resp2.status_code == 400
    assert 'erro' in resp2.json
    assert 'já existe' in resp2.json['erro']

def test_obter_atividade_para_professor(client, mock_professor_service):
    atividade = {"id_professor": 101, "enunciado": "Atividade específica"}
    post = client.post("/api/atividades/", json=atividade)
    id_atividade = post.json['id_atividade']

    # Professor correto recebe respostas
    resp_correto = client.get(f"/api/atividades/{id_atividade}/professor/101")
    assert resp_correto.status_code == 200
    assert 'respostas' in resp_correto.json

    # Outro professor não vê respostas completas
    resp_outro = client.get(f"/api/atividades/{id_atividade}/professor/202")
    assert resp_outro.status_code == 200
    assert 'respostas' not in resp_outro.json

# Teste extra: POST com professor não existente deve retornar 404
def test_criar_com_professor_inexistente(client, mock_professor_service):
    # Sobrescreve para retornar 404
    mock_professor_service.get(f"{PESSOA_SERVICE_URL}/999", status_code=404)
    data = {"id_professor": 999, "enunciado": "Teste erro professor"}
    resp = client.post("/api/atividades/", json=data)
    assert resp.status_code == 404
    assert 'erro' in resp.json
    assert 'Professor não encontrado' in resp.json['erro']