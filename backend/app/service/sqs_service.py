import json
import logging

import boto3
from botocore.exceptions import NoCredentialsError, PartialCredentialsError
from dotenv import load_dotenv

load_dotenv()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class SQSService:
    def __init__(self, queue_name: str, region_name: str = "us-east-1", use_localstack: bool = False):
        if use_localstack:
            self.sqs = boto3.client(
                "sqs",
                region_name=region_name,
                endpoint_url="http://localhost:4566",
                aws_access_key_id="test",
                aws_secret_access_key="test"
            )
        else:
            self.sqs = boto3.client("sqs", region_name=region_name)
        self.queue_name = queue_name
        self.queue_url = self.get_queue_url()

    def get_queue_url(self):
        try:
            response = self.sqs.get_queue_url(QueueName=self.queue_name)
            return response["QueueUrl"]
        except (NoCredentialsError, PartialCredentialsError) as e:
            logger.error("AWS credentials not found or incomplete: %s", e)
            raise
        except self.sqs.exceptions.QueueDoesNotExist:
            logger.info("Queue does not exist, creating a new one.")
            response = self.sqs.create_queue(QueueName=self.queue_name)
            return response["QueueUrl"]

    async def send_message(self, message_body: dict):
        logger.info(f"🔔 Enviando mensagem ao SQS: {message_body}")
        try:
            response = self.sqs.send_message(
                QueueUrl=self.queue_url,
                MessageBody=json.dumps(message_body)
            )
            logger.info("Message sent to SQS: %s", response["MessageId"])
        except Exception as e:
            logger.error("Failed to send message to SQS: %s", e)
            raise

    def receive_messages(self, max_messages: int = 10):
        try:
            response = self.sqs.receive_message(
                QueueUrl=self.queue_url,
                MaxNumberOfMessages=max_messages,
                WaitTimeSeconds=10
            )
            return response.get("Messages", [])
        except Exception as e:
            logger.error("Failed to receive messages from SQS: %s", e)
            raise

    def delete_message(self, receipt_handle: str):
        try:
            self.sqs.delete_message(
                QueueUrl=self.queue_url,
                ReceiptHandle=receipt_handle
            )
            logger.info("Message deleted from SQS")
        except Exception as e:
            logger.error("Failed to delete message from SQS: %s", e)
            raise
