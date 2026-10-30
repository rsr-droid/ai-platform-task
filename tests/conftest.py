import boto3
import pytest
from moto import mock_aws

from src.aws.s3 import SERVICE_BUCKET


@pytest.fixture(autouse=True)
def aws_credentials(monkeypatch):
    monkeypatch.setenv("AWS_ACCESS_KEY_ID", "test")
    monkeypatch.setenv("AWS_SECRET_ACCESS_KEY", "test")
    monkeypatch.setenv("AWS_DEFAULT_REGION", "us-east-1")


@pytest.fixture
def s3_client():
    with mock_aws():
        s3_client = boto3.client("s3")
        s3_client.create_bucket(Bucket=SERVICE_BUCKET)
        bucket = boto3.resource("s3").Bucket(SERVICE_BUCKET)
        yield s3_client
        for obj in bucket.objects.all():
            obj.delete()
        bucket.delete()
