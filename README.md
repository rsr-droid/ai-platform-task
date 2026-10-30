# Welcome!
And thank you for applying to join the AI Platform team!

The task you are about to complete is a simplified version of the kind of work carried out by the AI Platform team. In this repository, a prompt sync migration tool has already been implemented. Your task is to extend it with **dry-run** functionality.

## Prerequisites
### Python 3.10+
- [Mac](https://www.python.org/downloads/macos/)
- [Windows](https://www.python.org/downloads/windows/)
- [Other Platforms](https://www.python.org/download/other/)

### Docker
- Install Docker Desktop or another Docker engine.
  - [Mac](https://docs.docker.com/desktop/setup/install/mac-install/)
  - [Windows](https://docs.docker.com/desktop/setup/install/windows-install/)
  - [Linux](https://docs.docker.com/desktop/setup/install/linux/)
- Ensure Docker is running.

### Start LocalStack
1. Open a terminal in the same directory as `docker-compose.yaml`.
2. Run the following command:
   ```bash
   docker-compose up -d
   ```
   This will launch the LocalStack container in detached mode.

## Local Development Environment Setup
1. Create a virtual environment:
   ```bash
   python -m venv .venv
   ```
   If the above fails with `command not found: python`, try running:
   ```bash
   python3 -m venv .venv
   ```
2. Activate the virtual environment:
   ```bash
   source .venv/bin/activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Make the code available as an editable install:
   ```bash
   pip install -e .
   ```
5. Run the sync tool:
   ```bash
   python src/prompt_service/sync.py 'llm_chat'
   ```

   If running the script fails with `ModuleNotFoundError: No module named 'src'`, you may need to set the project root on the Python path, e.g.:
   ```bash
   export PYTHONPATH="$PWD"
   ```

6. Run tests (all tests should pass):
   ```bash
   pytest .
   ```

## Task Instructions
### Background
The prompt sync migration tool in `/src/prompt_service/sync.py` synchronises local prompt files with an S3 bucket. It supports uploading new files, deleting orphaned remote files, and updating files whose contents have changed.

Your task is to add a **dry-run mode** to this tool.

### Dry-Run Mode
When dry-run mode is enabled, the sync tool should **not** perform any S3 write operations (no uploads, no deletes). Instead, it should log a message for every action it **would have** taken.

The dry-run should be triggered by passing an optional `--dry-run` flag:
```bash
python src/prompt_service/sync.py 'llm_chat' --dry-run
```

### Requirements
1. The `PromptSync` class in `sync.py` must accept a `dry_run` parameter.
2. When `dry_run` is `True`:
   1. No files are uploaded to or deleted from S3.
   2. For each file that **would be uploaded**, a log message is emitted: `Would upload <key>` (e.g. `Would upload llm_chat/system_prompt.txt`).
   3. For each file that **would be deleted**, a log message is emitted: `Would delete <key>` (e.g. `Would delete llm_chat/old_prompt.txt`).
3. When `dry_run` is `False` (the default), the tool behaves exactly as it does today — files are uploaded and deleted normally.
4. The CLI entry point (`if __name__ == "__main__"`) must accept an optional `--dry-run` flag and pass it through to `PromptSync`.
5. All existing tests must continue to pass.
6. Formatting and linting checks must be run and issues addressed.

### Requirements
1. All tests must pass.
2. Formatting and linting checks must be run and issues addressed.

## Repository Contents
- `.flake8` settings for flake8
- `.gitignore`
- `docker-compose.yaml` for pulling and running LocalStack
- `pyproject.toml` formatter settings
- `README.md`
- `requirements.txt`
- `/src`
  - `/aws`
    - `s3.py` provides an S3 client connected to LocalStack with `ensure_bucket_exists()`
  - `/features`
    - `/llm_chat`
      - `client.py` a dummy implementation of a chat client
      - `/prompts`
        - `system_prompt.txt`
        - `user_prompt.txt`
  - `/prompt_service`
    - `sync.py` the prompt sync migration tool with `PromptSync` class
  - `main.py` a CLI tool that calls the LLM Chat client
- `/tests`
  - `conftest.py` shared fixtures including a moto-backed `s3_client`
  - `/integration`
    - `test_ai_platform.py` integration test using S3 on LocalStack
  - `/unit`
    - `/aws`
      - `test_s3.py` tests for the S3 client and `ensure_bucket_exists`
    - `/prompt_service`
      - `test_sync.py` unit tests for `PromptSync`
    - `test_main.py` test that the main entry point passes a message to the chat client

## Formatting & Linting
1. Sort imports:
   ```bash
   isort .
   ```
2. Format the code:
   ```bash
   black .
   ```
3. Run lint checks:
   ```bash
   flake8 .
   ```