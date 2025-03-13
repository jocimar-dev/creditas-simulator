# Credit Simulator API

## Overview
This project is a **FastAPI-based Credit Simulator API** that allows users to simulate loans based on their birthdate, loan amount, and payment duration.

## Features
- Simulates loan payments based on different interest rates.
- Calculates total payment, interest paid, and monthly installment.
- Provides a RESTful API with **FastAPI**.
- Uses **Poetry** for dependency management.
- Dockerized using **Docker & Docker Compose**.
- Includes **automated tests** using **Pytest**.
- Utilizes **LocalStack** for local AWS service emulation.
- Supports asynchronous methods and testing.

---

## Requirements
Ensure you have the following installed:
- [Python 3.12+](https://www.python.org/downloads/)
- [Poetry](https://python-poetry.org/docs/)
- [Docker](https://www.docker.com/) & [Docker Compose](https://docs.docker.com/compose/)

---

## Installation & Running Locally

### 1️⃣ **Clone the Repository**
```sh
 git clone https://github.com/jocimar-dev/creditas-simulator
 cd creditas-simulator
```

### 2️⃣ **Install Dependencies with Poetry**
```sh
poetry install
```

**Load Environment Variables**

Make sure the `.env `file is in the root of your project and contains all the necessary environment variables
```.env
# Ambiente de desenvolvimento
ENV=dev

# Configurações do LocalStack
export USE_LOCALSTACK=true
export AWS_ACCESS_KEY_ID=test
export AWS_SECRET_ACCESS_KEY=test
export AWS_DEFAULT_REGION=us-east-1

# URL da fila SQS no LocalStack
SQS_QUEUE_URL=http://localhost:4566/000000000000/loan-simulation-queue

# Configurações do servidor SMTP para envio de emails
SMTP_SERVER=sandbox.smtp.mailtrap.io
SMTP_PORT=587
SMTP_USERNAME=c982143cf59649
SMTP_PASSWORD=190529bb785a7e

# Nome da fila SQS e região AWS
SQS_QUEUE_NAME=loan_simulation_queue
AWS_REGION=us-east-1

# Configurações de simulação
USE_SIMULATED_RATE=true
SIMULATED_INTEREST_RATE=0.015
USE_SIMULATED_CONVERSION=true
USE_SIMULATED_EMAIL=true

#Token JWT
JWT_SECRET=secret_creditas
JWT_ALGORITHM=HS256
```
### 3️⃣ **Run the API Locally**
```sh
poetry run uvicorn app.main:app --reload
```

The API should be available in Swagger at: **[http://localhost:8000/docs](http://localhost:8000/docs)**

---

## Running with Docker

### **Build & Start the Docker Container**
```sh
docker-compose up --build
```

### **Stop the Container**
```sh
docker-compose down
```

---

## API Endpoints

### **1️⃣ Health Check**
`GET /health`
#### **Response**
```json
{
  "status": "ok"
}
```

### **2️⃣ Loan Simulation**
`POST /simulate`
`POST /v2/simulate`
`POST /v2/simulate/batch`

#### **Request Body**
```json
{
  "principal_data": {
    "loan_amount": 10000.0,
    "birth_date": "1985-06-10",
    "installment": 12,
    "interest_rate_type": "fixed",
    "currency": "BRL"
  },
  "personal_request": {
    "full_name": "Jocimar Neres",
    "document_number": "12345678900",
    "marital_status": "single",
    "dependents": 1
  },
  "contact_request": {
    "address": "Rua Exemplo, 123",
    "phone": "+55 11 91234-5678",
    "email": "jocimarneres@gmail.com"
  },
  "financial_request": {
    "monthly_income": 5000.00,
    "monthly_expenses": 2000.00,
    "real_estate_value": 150000.00,
    "vehicle_value": 40000.00
  }
}
```

#### **Response**
```json
{
    "full_name": "Jocimar Neres",
    "document_number_partial": "8900",
    "total_payment": 10300.0,
    "monthly_payment": 858.33,
    "total_interest": 300.0,
    "monthly_rate": 0.0025,
    "annual_rate": 0.03,
    "installment": 12,
    "guarantee_value": 190000.0
}
```

### **Curl Examples**
```sh
curl --location 'http://localhost:8000/simulate' \
--header 'Content-Type: application/json' \
--header 'accept: application/json' \
--data-raw '{
  "principal_data": {
    "loan_amount": 10000.0,
    "birth_date": "1985-06-10",
    "installment": 12,
    "interest_rate_type": "fixed",
    "currency": "BRL"
  },
  "personal_request": {
    "full_name": "Jocimar Neres",
    "document_number": "12345678900",
    "marital_status": "single",
    "dependents": 1
  },
  "contact_request": {
    "address": "Rua Exemplo, 123",
    "phone": "+55 11 91234-5678",
    "email": "jocimarneres@gmail.com"
  },
  "financial_request": {
    "monthly_income": 5000.00,
    "monthly_expenses": 2000.00,
    "real_estate_value": 150000.00,
    "vehicle_value": 40000.00
  }
}'
```

```sh
curl --location 'http://localhost:8000/v2/simulate' \
--header 'Content-Type: application/json' \
--header 'accept: application/json' \
--data-raw '{
  "principal_data": {
    "loan_amount": 10000.0,
    "birth_date": "1985-06-10",
    "installment": 12,
    "interest_rate_type": "fixed",
    "currency": "BRL"
  },
  "personal_request": {
    "full_name": "Jocimar Neres",
    "document_number": "12345678900",
    "marital_status": "single",
    "dependents": 1
  },
  "contact_request": {
    "address": "Rua Exemplo, 123",
    "phone": "+55 11 91234-5678",
    "email": "jocimarneres@gmail.com"
  },
  "financial_request": {
    "monthly_income": 5000.00,
    "monthly_expenses": 2000.00,
    "real_estate_value": 150000.00,
    "vehicle_value": 40000.00
  }
}'
```

```sh
curl --location 'http://localhost:8000/v2/simulate/batch' \
--header 'Content-Type: application/json' \
--header 'accept: application/json' \
--data-raw '[{
  "principal_data": {
    "loan_amount": 10000.0,
    "birth_date": "1985-06-10",
    "installment": 12,
    "interest_rate_type": "fixed",
    "currency": "BRL"
  },
  "personal_request": {
    "full_name": "Jocimar Neres",
    "document_number": "12345678900",
    "marital_status": "single",
    "dependents": 1
  },
  "contact_request": {
    "address": "Rua Exemplo, 123",
    "phone": "+55 11 91234-5678",
    "email": "jocimarneres@gmail.com"
  },
  "financial_request": {
    "monthly_income": 5000.00,
    "monthly_expenses": 2000.00,
    "real_estate_value": 150000.00,
    "vehicle_value": 40000.00
  }
}]'
```

---

## LocalStack
LocalStack is a fully functional local AWS cloud stack. It allows you to develop and test your cloud and serverless apps offline. In this project, LocalStack is used to emulate AWS SQS services locally.

### **Setup LocalStack**
LocalStack is configured in the `docker-compose.yml` file. It runs as a Docker container and provides endpoints for AWS services.

### **LocalStack Configuration**
```yaml
services:
  localstack:
    image: localstack/localstack:latest
    container_name: localstack
    ports:
      - "4566:4566"
      - "4571:4571"
    environment:
      - SERVICES=sqs
      - DEBUG=1
      - DATA_DIR=/tmp/localstack/data
      - INIT_SCRIPTS_PATH=/etc/localstack/init
    volumes:
      - ./localstack-data:/var/lib/localstack
      - ./localstack_tmp:/tmp/localstack_tmp
      - ./init-scripts:/etc/localstack/init
```

---

## Asynchronous Methods
Asynchronous programming is used to improve the performance of I/O-bound operations. In this project, asynchronous methods are used for processing loan simulations and sending emails.

### **Example of Asynchronous Method**
```python
@router.post("/simulate", response_model=LoanSimulationResponse)
async def simulate_loan(request: LoanSimulationRequest):
    response = await process_loan_simulation(request)
    asyncio.create_task(email_service.send_email(...))
    return response
```

---

## Asynchronous Testing
Asynchronous tests are written using `pytest` with the `pytest-asyncio` plugin. This allows you to test asynchronous code in a synchronous manner.

### **Example of Asynchronous Test**

```python
import pytest
from fastapi.testclient import TestClient
from app import app

client = TestClient(app)


@pytest.mark.asyncio
async def test_simulate_loan():
    response = await client.post("/simulate", json={...})
    assert response.status_code == 200
    assert response.json() == {...}
```

---

## SQS Integration
AWS SQS (Simple Queue Service) is used for message queuing. In this project, SQS is used to send and receive messages related to loan simulations.

### **SQS Service Example**
```python
class SQSService:
    async def send_message(self, message_body: dict):
        response = self.sqs.send_message(
            QueueUrl=self.queue_url,
            MessageBody=json.dumps(message_body)
        )
        return response
```

---

## Project Structure
```
credit_simulator/
│── app/
│   ├── adapters/
│   │   ├── mapper/        # Mapping logic for loan simulation and response
│   │   └── messaging/     # Email body generation logic
│   ├── core/
│   │   ├── configs/       # Configuration settings
│   │   └── constants/     # Constants and enums
│   ├── domain/
│   │   └── models/        # Domain models for contact, financial, personal, and principal data
│   ├── dtos/              # Data Transfer Objects for loan request and result
│   ├── factories/         # Factory classes for creating email and loan simulation instances
│   ├── routers/           # API route controllers
│   ├── service/
│   │   ├── messaging/     # Email and SQS services
│   │   └── simulation/    # Loan simulation services
│   ├── validators/        # Validation logic for authentication and loan simulation
│   └── main.py            # Main application entry point
│── docs/                  # Documentation files
│── init-scripts/          # Initialization scripts
│── tests/                 # Test cases for the application
│── Dockerfile             # Docker configuration
│── README.md              # Project README file
│── docker-compose.yml     # Docker Compose configuration
│── poetry.lock            # Poetry lock file
│── pyproject.toml         # Poetry project configuration
│── pytest.ini             # Pytest configuration
```

### **Architecture Decisions**
- **FastAPI**: Chosen for its high performance and ease of use.
- **Poetry**: Used for dependency management to ensure consistent environments.
- **Docker & Docker Compose**: Used for containerization and easy setup of development environments.
- **LocalStack**: Used to emulate AWS services locally for development and testing.
- **Asynchronous Programming**: Used to handle I/O-bound operations efficiently.

---

## Running Tests
To execute automated tests:
```sh
pytest tests/
```

---

## Business rules, architecture and technical decisions
For detailed explanations of business rules, architecture and technical decisions, see the document [Business rules and architecture](docs/business_rules_architecture.md) in English or [Regras de Negócio e Arquitetura](docs/regras_negocio_arquitetura.md) in Portuguese.

---

## License
This project is under the **MIT License**.

---

## Contributors
- Jocimar Neres - [GitHub](https://github.com/jocimar-dev)