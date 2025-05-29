# API de Atividades

Este repositório contém a API de Atividades, desenvolvida com Flask e SQLAlchemy, como parte de uma arquitetura baseada em microsserviços.

---

## 🧩 Arquitetura

A API de Atividades é um microsserviço responsável pelo gerenciamento de atividades de professores. Ela faz parte de um sistema maior (School System), onde cada microsserviço desempenha um papel específico:

* **atividade\_service**: gerencia CRUD de atividades.
* **escola\_service**: (API de Escola) gerencia Professores, Alunos e Turmas.

A comunicação entre os serviços ocorre via HTTP REST. Antes de criar uma atividade, o `atividade_service` realiza uma chamada GET para:

```
GET {PESSOA_SERVICE_URL}/{id_professor}
```

para validar a existência do professor.

---

## 🚀 Tecnologias Utilizadas

* Python 3.13
* Flask 3.1.0
* Flask-SQLAlchemy 3.1.1
* SQLite (banco de dados local)
* Requests (para consumo da API de Escola)
* Gunicorn 20.1.0
* Docker & Docker Compose
* Pytest + requests-mock para testes automatizados

---

## ▶️ Como Executar a API

1. **Clone o repositório**:

   ```bash
   git clone https://github.com/Skyiver/devapiatividade.git
   cd Desenvolvimento-de-APIs-Atividades
   ```

2. **Verifique o arquivo `docker-compose.yml`**:

   * Certifique-se de que a rede do Docker Compose inclua também o serviço da API de Escola.

   * Adicione na seção `environment` do serviço `web` a variável:

     ```yaml
     environment:
       - PESSOA_SERVICE_URL=http://escola:5002/api/professores
     ```

   * Exemplo mínimo:

     ```yaml
     services:
       escola:
         image: escola-service:latest
         container_name: escola
         ports:
           - "5002:5002"

       atividade-web:
         build: .
         container_name: atividade-web
         ports:
           - "5001:5001"
         environment:
           - FLASK_ENV=development
           - DATABASE_URL=sqlite:////app/atividades.db
           - PESSOA_SERVICE_URL=http://escola:5002/api/professores
         depends_on:
           - escola
     ```

3. **Suba os serviços**:

   ```bash
   docker-compose up --build
   ```

4. **Acesse a API**:

   * Base URL: `http://localhost:5001/api/atividades`

---

## 📡 Endpoints Principais

* `GET /api/atividades/` – Lista todas as atividades (retorna resumo sem respostas).
* `POST /api/atividades/` – Cria uma nova atividade. Exemplo de JSON:

  ```json
  {
    "id_professor": 1,
    "enunciado": "Desenvolver API RESTful"
  }
  ```
* `GET /api/atividades/<id>` – Detalha uma atividade (inclui lista de respostas).
* `GET /api/atividades/<id_atividade>/professor/<id_professor>` – Detalha atividade para um professor específico. Se o `id_professor` informado não for o autor, retorna apenas resumo (sem respostas).

---

## 📦 Estrutura do Projeto

```
atividade-service/
│
├── atividade_service/
│   ├── controllers/
│   │   └── atividade_controller.py
│   ├── models/
│   │   └── atividade.py
│   ├── services/
│   │   ├── atividade_service.py
│   │   └── pessoa_service_client.py
│   ├── tests/
│   │   └── test_atividades.py
│   ├── app.py
│   └── config.py
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── README.md
```

---

## 🛠️ Testes Automatizados

Os testes estão em `atividade_service/tests/test_atividades.py` e cobrem:

* Listagem vazia e após criação
* Obtenção de atividade existente
* Criação com ID duplicado
* Teste de integração simulada com a API de Escola (requests-mock)
* Criação com professor inexistente (retorno 404)

Para rodar:

```bash
pytest -v
```

---

## 🛠️ Futuras Melhorias

* Healthcheck que valide dependência da API de Escola.
* Endpoint de retry/fallback em caso de indisponibilidade da API de Escola.
* Autenticação e autorização (JWT/OAuth).

---

## 🧑‍💻 Autores

* Akira Ogassavara (Curso de SI – Impacta)
* Amanda Costa (Curso de SI – Impacta)