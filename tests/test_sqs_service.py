import os
import boto3
import pytest
from moto import mock_aws
from app import SQSService


@pytest.fixture
def sqs_service():
    with mock_aws():
        sqs = boto3.client("sqs", region_name="us-east-1")
        queue_url = sqs.create_queue(QueueName="test-queue")["QueueUrl"]
        os.environ["SQS_QUEUE_URL"] = queue_url
        return SQSService(queue_name="test-queue", use_localstack=True)


@pytest.mark.asyncio
async def test_send_message(sqs_service):
    response = await sqs_service.send_message({"message": "Test message"})
    assert response["ResponseMetadata"]["HTTPStatusCode"] == 200


@pytest.mark.asyncio
async def test_receive_messages(sqs_service):
    await sqs_service.send_message({"message": "Test message"})
    messages = await sqs_service.receive_messages()
    # Verifica se há mensagens na fil
    assert len(messages) > 0
    assert messages[0]["Body"] == '{"message": "Test message"}'


@pytest.mark.asyncio
async def test_delete_message(sqs_service):
    await sqs_service.send_message({"message": "Test message"})

    # Recebe a mensagem
    messages = await sqs_service.receive_messages()
    assert len(messages) > 0

    receipt_handle = messages[0]["ReceiptHandle"]

    # Deleta a mensagem corretamente
    await sqs_service.delete_message(receipt_handle)

    # Lê de novo a fila para verificar se foi deletada
    messages_after = await sqs_service.receive_messages()

    # ✅ Espera que não haja mensagens restantes da mesma
    assert all(msg["ReceiptHandle"] != receipt_handle for msg in messages_after)
