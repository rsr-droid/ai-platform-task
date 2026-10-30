from unittest.mock import patch

from src.aws.s3 import SERVICE_BUCKET, ensure_bucket_exists, s3_client


def test_s3_client_endpoint():
    expected_endpoint = "http://localhost:4566"
    assert s3_client._endpoint.host == expected_endpoint


def test_s3_client_service():
    assert s3_client.meta.service_model.service_name == "s3"


def test_ensure_bucket_exists_creates_bucket_when_missing(s3_client):
    s3_client.delete_bucket(Bucket=SERVICE_BUCKET)

    with patch("src.aws.s3.s3_client", s3_client):
        ensure_bucket_exists()

    s3_client.head_bucket(Bucket=SERVICE_BUCKET)


def test_ensure_bucket_exists_does_not_fail_when_bucket_exists(s3_client):
    with patch("src.aws.s3.s3_client", s3_client):
        ensure_bucket_exists()

    s3_client.head_bucket(Bucket=SERVICE_BUCKET)
