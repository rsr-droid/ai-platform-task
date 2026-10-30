from unittest.mock import MagicMock, patch

from src.main import main


def test_main():
    with patch("src.main.ensure_bucket_exists"), patch("src.main.LLMChatClient") as mock_llm_chat_client_cls:
        mock_llm_chat_client_cls.return_value = MagicMock()
        mock_llm_chat_client_cls.return_value.chat.return_value = "Mocked Chat Response"
        main("Test message")

    mock_llm_chat_client_cls.return_value.chat.assert_called_once_with("Test message")
