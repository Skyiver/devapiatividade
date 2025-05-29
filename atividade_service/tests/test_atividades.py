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
    app = create_app()
    app.register_blueprint(atividade_bp, url_prefix='/api/atividades')
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
        yield client

@pytest.fixture
def mock_professor_service():
    with requests_mock.Mocker() as m:
        # Corrigido: regex compatível com a URL real do serviço
        url_pattern = re.compile(f"{re.escape(PESSOA_SERVICE_URL)}/professor/\\d+")
        m.get(url_pattern, 
              json=lambda request, context: {
                  "id": int(request.url.split('/')[-1]),
                  "tipo": "professor"
              }, 
              status_code=200)
        yield m

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
    response = client.post("/api/atividades/", json=nova_atividade)
    assert response.status_code == 201
    id_atividade = response.json['id_atividade']

    response = client.get("/api/atividades/")
    assert response.status_code == 200
    assert len(response.json) == 1
    assert response.json[0]['id_atividade'] == id_atividade

def test_obter_atividade_existente(client, mock_professor_service):
    nova_atividade = {
        "id_professor": 101,
        "enunciado": "Desenvolver API RESTful"
    }
    response = client.post("/api/atividades/", json=nova_atividade)
    id_atividade = response.json['id_atividade']

    response = client.get(f"/api/atividades/{id_atividade}")
    assert response.status_code == 200
    assert response.json['id_atividade'] == id_atividade
    assert response.json['enunciado'] == "Desenvolver API RESTful"

def test_criar_atividade_id_duplicado(client, mock_professor_service):
    atividade = {
        "id_atividade": 1001,  # ID fixo para evitar conflitos
        "id_professor": 101,
        "enunciado": "Primeira atividade"
    }
    
    # Primeira criação
    response1 = client.post("/api/atividades/", json=atividade)
    assert response1.status_code == 201
    
    # Segunda criação com mesmo ID
    response2 = client.post("/api/atividades/", json=atividade)
    assert response2.status_code == 400
    assert 'erro' in response2.json
    assert 'já existe' in response2.json['erro']

def test_obter_atividade_para_professor(client, mock_professor_service):
    atividade = {
        "id_professor": 101,
        "enunciado": "Atividade específica"
    }
    response = client.post("/api/atividades/", json=atividade)
    id_atividade = response.json['id_atividade']

    # Professor correto
    response = client.get(f"/api/atividades/{id_atividade}/professor/101")
    assert response.status_code == 200
    assert 'respostas' in response.json

    # Outro professor
    response = client.get(f"/api/atividades/{id_atividade}/professor/202")
    assert response.status_code == 200
    assert 'respostas' not in response.json