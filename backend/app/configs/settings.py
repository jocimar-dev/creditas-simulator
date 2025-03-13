import boto3
from botocore.config import Config
import os

config = Config(
    region_name='us-east-1',
    signature_version='v4',
    retries={
        'max_attempts': 10,
        'mode': 'standard'
    }
)

sqs = boto3.client('sqs', config=config, aws_access_key_id='test', aws_secret_access_key='test', endpoint_url='http://localhost:4566')


USE_LOCALSTACK = os.getenv("USE_LOCALSTACK", "true").lower() == "true"
