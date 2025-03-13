#!/bin/bash
echo "🚀 Criando fila no LocalStack..."
aws --endpoint-url=http://localhost:4566 sqs create-queue --queue-name loan_simulation_queue
