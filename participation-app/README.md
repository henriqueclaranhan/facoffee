# FACOFFEE - Serviço de Cotas

Este é o serviço de domínio **Participation**, construído com **FastAPI** e utilizando os princípios de **Domain-Driven Design (DDD)** e **Clean Architecture**.


## Arquitetura e DDD


```
participation/
├── app/
│   ├── core/                  # Segurança, decodificação JWT e middlewares comuns
│   ├── domain/                # Coração do negócio (regras e invariantes)
│   │   ├── models/            # Entidades do Domínio & Value Objects (ex: ParticipationQuota)
│   │   ├── exceptions/        # Exceções de Domínio (ex: InvalidQuotaDataException)
│   │   └── repositories/      # Interfaces de Repositório (Abstrações)
│   ├── application/           # Casos de Uso (Orquestração do fluxo)
│   │   ├── use_cases/         # Casos de uso de negócio (ex: CreateQuotaUseCase)
│   │   └── dtos/              # Objetos de Transferência de Dados (Pydantic)
│   ├── infrastructure/        # Detalhes de tecnologia e infraestrutura externa
│   │   └── database/          # Configuração SQLAlchemy, Models DB, Repositórios concretos
│   └── presentation/          # Entrada HTTP e roteamento HTTP (FastAPI Routers)
├── tests/                     # Suíte de testes automatizados
│   ├── unit/                  # Testes das regras de validação do domínio
│   └── integration/           # Testes integrados de endpoints com banco em memória
└── requirements.txt           # Dependências do Python
```

## Tecnologias

- **Python 3.12+**
- **FastAPI** (Framework web de alta performance)
- **SQLAlchemy 2.0** (ORM robusto para persistência)
- **SQLite** (Banco de dados relacional leve para desenvolvimento)
- **PyJWT & Cryptography** (Decodificação e validação de tokens JWT)
- **Pytest** (Suíte de testes automatizados de alta performance)


## Como Rodar

### 1) Pré-requisitos
```bash
# Na pasta raiz do facoffee
docker compose up -d
```

### 2) Criação e ativação do Ambiente Virtual (venv)
Entre na pasta `participation-app` e crie a venv:
```powershell
cd participation
python -m venv .venv
```

No Windows:
```cmd
.venv\Scripts\activate.bat
```

No Linux:
```bash
source .venv/bin/activate
```

### 3) Instalação das Dependências
Com o ambiente ativado, instale as dependências:
```bash
pip install -r requirements.txt
```

### 4) Executando a Aplicação
```bash
uvicorn app.main:app --host 0.0.0.0 --port 3002 --reload
```

## Testes Automatizados

```bash
# Com a venv ativa na pasta participation
pytest
```

## Endpoints Disponíveis

Os endpoints seguem a convenção do contrato OpenAPI `api-docs.yaml`:

### 1. Cadastrar Cota de Participação

### 2. Listar Cotas de Participação


## To-do:
* Docker do app