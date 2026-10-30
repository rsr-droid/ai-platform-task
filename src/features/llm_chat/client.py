from botocore.exceptions import ClientError

from src.aws.s3 import SERVICE_BUCKET
from src.features.llm_chat import FEATURE_NAME


class LLMChatClient:
    def __init__(self, s3_client):
        self._s3_client = s3_client
        self._system_prompt = None
        self._user_prompt = None

    def chat(self, message):
        return f"System prompt: {self.system_prompt}\nUser prompt: {self.user_prompt}\nMessage: {message}"

    @property
    def system_prompt(self):
        if not self._system_prompt:
            self._system_prompt = self._load_system_prompt()
        return self._system_prompt

    def _load_system_prompt(self):
        try:
            response = self._s3_client.get_object(Bucket=SERVICE_BUCKET, Key=f"{FEATURE_NAME}/system_prompt.txt")
            return response["Body"].read().decode("utf-8")
        except ClientError:
            return f"System prompt not found on {SERVICE_BUCKET}"

    @property
    def user_prompt(self):
        if not self._user_prompt:
            self._user_prompt = self._load_user_prompt()
        return self._user_prompt

    def _load_user_prompt(self):
        try:
            response = self._s3_client.get_object(Bucket=SERVICE_BUCKET, Key=f"{FEATURE_NAME}/user_prompt.txt")
            return response["Body"].read().decode("utf-8")
        except ClientError:
            return f"User prompt not found on {SERVICE_BUCKET}"
