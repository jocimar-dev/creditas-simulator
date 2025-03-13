import boto3
import os

def test_sqs():
    # Configurações do SQS
    queue_name = "test-queue"
    region_name = "us-east-1"
    endpoint_url = "http://localhost:4566"

    # Criação do cliente SQS
    sqs = boto3.client(
        "sqs",
        region_name=region_name,
        endpoint_url=endpoint_url,
        aws_access_key_id="test",
        aws_secret_access_key="test"
    )

    # Criação da fila
    response = sqs.create_queue(QueueName=queue_name)
    queue_url = response["QueueUrl"]
    print(f"Fila criada: {queue_url}")

    # Envio de mensagem
    message_body = {"message": "Hello, SQS!"}
    response = sqs.send_message(
        QueueUrl=queue_url,
        MessageBody=str(message_body)
    )
    print(f"Mensagem enviada. ID: {response['MessageId']}")

    # Recebimento de mensagem
    response = sqs.receive_message(
        QueueUrl=queue_url,
        MaxNumberOfMessages=1,
        WaitTimeSeconds=10
    )
    messages = response.get("Messages", [])
    if messages:
        for message in messages:
            print(f"Mensagem recebida: {message['Body']}")
            # Deleção da mensagem
            sqs.delete_message(
                QueueUrl=queue_url,
                ReceiptHandle=message["ReceiptHandle"]
            )
            print("Mensagem deletada.")
    else:
        print("Nenhuma mensagem recebida.")

if __name__ == "__main__":
    test_sqs()