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
`GET /`
#### **Response**
```json
{
  "status": "Ok"
}
```

### **2️⃣ Loan Simulation**
`POST /simulate`
#### **Request Body**
```json
{
  "loan_amount": 10000,
  "birth_date": "1990-05-15",
  "months": 12
}
```
#### **Response**
```json
{
  "loan_amount": 10000,
  "months": 12,
  "interest_rate": 3.0,
  "results": {
    "monthly_payment": 850.0,
    "total_payment": 10200.0,
    "total_interest": 200.0
  }
}
```

---

## Running Tests
To execute automated tests:
```sh
pytest tests/
```

---

## Project Structure
```
credit_simulator/
│── app/
│   ├── main.py         # API entry point
│   ├── routes.py       # API endpoints
│   ├── models.py       # Request models
│   ├── services.py     # Business logic
│── tests/              # Test cases
│── Dockerfile          # Docker container setup
│── docker-compose.yml  # Docker Compose configuration
│── pyproject.toml      # Poetry dependencies
│── README.md           # Project documentation
```

---

## License
This project is under the **MIT License**.

---

## Contributors
- Jocimar Neres - [GitHub](https://github.com/jocimar-dev)
