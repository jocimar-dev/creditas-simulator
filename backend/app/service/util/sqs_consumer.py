import boto3
import os

def list_messages_from_queue():
    sqs = boto3.client(
        'sqs',
        region_name=os.getenv("AWS_REGION", "us-east-1"),
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID", "test"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY", "test"),
        endpoint_url=os.getenv("SQS_ENDPOINT_URL", "http://localhost:4566")
    )
    queue_url = os.getenv("SQS_QUEUE_URL")

    response = sqs.receive_message(
        QueueUrl=queue_url,
        MaxNumberOfMessages=10,  # Número máximo de mensagens a serem recebidas
        WaitTimeSeconds=10  # Tempo de espera para receber mensagens
    )

    messages = response.get('Messages', [])
    for message in messages:
        print(f"Message ID: {message['MessageId']}")
        print(f"Message Body: {message['Body']}")
        print("----")

if __name__ == "__main__":
    list_messages_from_queue()