import boto3
from botocore.exceptions import ClientError

SERVICE_BUCKET = "ai-platform"


s3_client = boto3.client(
    "s3",
    region_name="us-east-1",
    aws_access_key_id="local_access_key",
    aws_secret_access_key="local_secret_key",
    endpoint_url="http://localhost:4566",
)


def ensure_bucket_exists() -> None:
    try:
        s3_client.head_bucket(Bucket=SERVICE_BUCKET)
    except ClientError:
        s3_client.create_bucket(Bucket=SERVICE_BUCKET)
