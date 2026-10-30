from src.aws.s3 import SERVICE_BUCKET
from src.prompt_service.sync import PromptSync


def test_sync_uploads_local_files_not_on_s3(s3_client, tmp_path):
    prompts_dir = tmp_path / "prompts"
    prompts_dir.mkdir()
    (prompts_dir / "prompt_a.txt").write_text("content a")

    PromptSync(s3_client, "my_feature", prompts_dir).sync()

    body = s3_client.get_object(Bucket=SERVICE_BUCKET, Key="my_feature/prompt_a.txt")["Body"].read().decode()
    assert body == "content a"


def test_sync_deletes_s3_files_not_local(s3_client, tmp_path):
    s3_client.put_object(Bucket=SERVICE_BUCKET, Key="my_feature/old_prompt.txt", Body=b"old")
    prompts_dir = tmp_path / "prompts"
    prompts_dir.mkdir()

    PromptSync(s3_client, "my_feature", prompts_dir).sync()

    response = s3_client.list_objects_v2(Bucket=SERVICE_BUCKET, Prefix="my_feature/")
    assert response.get("Contents") is None


def test_sync_uploads_file_when_content_differs(s3_client, tmp_path):
    s3_client.put_object(Bucket=SERVICE_BUCKET, Key="my_feature/prompt.txt", Body=b"old content")
    prompts_dir = tmp_path / "prompts"
    prompts_dir.mkdir()
    (prompts_dir / "prompt.txt").write_text("new content")

    PromptSync(s3_client, "my_feature", prompts_dir).sync()

    body = s3_client.get_object(Bucket=SERVICE_BUCKET, Key="my_feature/prompt.txt")["Body"].read().decode()
    assert body == "new content"


def test_sync_skips_upload_when_content_matches(s3_client, tmp_path):
    s3_client.put_object(Bucket=SERVICE_BUCKET, Key="my_feature/prompt.txt", Body=b"same content")
    prompts_dir = tmp_path / "prompts"
    prompts_dir.mkdir()
    (prompts_dir / "prompt.txt").write_text("same content")

    PromptSync(s3_client, "my_feature", prompts_dir).sync()

    body = s3_client.get_object(Bucket=SERVICE_BUCKET, Key="my_feature/prompt.txt")["Body"].read().decode()
    assert body == "same content"
