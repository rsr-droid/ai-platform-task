import argparse
from pathlib import Path
import logging
import re

from src.aws.s3 import SERVICE_BUCKET, ensure_bucket_exists, s3_client

FEATURES_DIR = Path(__file__).parent.parent / "features"

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class PromptSync:
    def __init__(self, s3_client, feature_name: str, prompts_dir: Path, dry_run: bool = False) -> None:
        self._s3_client = s3_client
        self._feature_name = feature_name
        self._prompts_dir = prompts_dir
        self._dry_run = dry_run        

    def sync(self) -> None:
        local_files = {f.name for f in self._prompts_dir.glob("*.txt")}
        remote_files = self._get_remote_files()

        for filename in remote_files - local_files:
            self._delete_file(filename)

        for filename in local_files - remote_files:
            self._upload_file(filename)

        for filename in local_files & remote_files:
            local_content = (self._prompts_dir / filename).read_text()
            response = self._s3_client.get_object(Bucket=SERVICE_BUCKET, Key=self._make_key(filename))
            remote_content = response["Body"].read().decode("utf-8")
            if local_content != remote_content:
                self._upload_file(filename)

    def _make_key(self, filename: str) -> str:
        return f"{self._feature_name}/{filename}"

    def _get_remote_files(self) -> set[str]:
        prefix = f"{self._feature_name}/"
        response = self._s3_client.list_objects_v2(Bucket=SERVICE_BUCKET, Prefix=prefix)
        return {obj["Key"].removeprefix(prefix) for obj in response.get("Contents", [])}

    def _upload_file(self, filename: str) -> None:
        key = self._make_key(filename)
        if self._dry_run:
            logger.info(f"Would upload: {key}")
            return
        self._s3_client.upload_file(str(self._prompts_dir / filename), SERVICE_BUCKET, self._make_key(filename))

    def _delete_file(self, filename: str) -> None:
        key = self._make_key(filename)
        if self._dry_run:
            logger.info(f"Would delete: {key}")
            return
        self._s3_client.delete_object(Bucket=SERVICE_BUCKET, Key=self._make_key(filename))


def main(feature_name: str, dry_run: bool = False) -> None:
    ensure_bucket_exists()
    prompts_dir = FEATURES_DIR / feature_name / "prompts"
    PromptSync(s3_client, feature_name, prompts_dir, dry_run=dry_run).sync()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Prompt sync migration tool")
    parser.add_argument("feature_name", type=str, help="The feature to sync prompts for")
    parser.add_argument(
        "--dry-run",
        action='store_true',
        help='Preview changes without uploading or deleting'
    )
    args = parser.parse_args()
    main(args.feature_name, args.dry_run)
