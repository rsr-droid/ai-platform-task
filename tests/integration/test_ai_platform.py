import boto3
import pytest

from src.aws.s3 import SERVICE_BUCKET, s3_client
from src.features.llm_chat import FEATURE_NAME
from src.main import main as send_chat_message
from src.prompt_service.sync import main as prompt_sync


@pytest.fixture
def localstack_setup_teardown():
    s3_client.create_bucket(Bucket=SERVICE_BUCKET)
    bucket = boto3.resource(
        "s3",
        region_name="us-east-1",
        aws_access_key_id="local_access_key",
        aws_secret_access_key="local_secret_key",
        endpoint_url="http://localhost:4566",
    ).Bucket(SERVICE_BUCKET)
    yield
    for obj in bucket.objects.all():
        obj.delete()
    bucket.delete()


@pytest.mark.usefixtures("localstack_setup_teardown")
def test_sync_updates_llm_chat_prompts():
    original_output = send_chat_message("Test message")

    prompt_sync(FEATURE_NAME)
    updated_output = send_chat_message("Test message")

    assert original_output == (
        "System prompt: System prompt not found on ai-platform\n"
        "User prompt: User prompt not found on ai-platform\n"
        "Message: Test message"
    ), "Expected original output to indicate prompts not found"
    assert updated_output == (
        "System prompt: A test system prompt.\n" "User prompt: A test user prompt.\n" "Message: Test message"
    ), "Expected updated output to reflect the new prompts"
