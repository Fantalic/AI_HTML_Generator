import pytest
from ai_creature_generator.services.ollama import ai_request


def test_requires_model():
    with pytest.raises(ValueError, match="Model is required"):
        ai_request(model=None)


def test_chat_requires_messages():
    with pytest.raises(ValueError, match="Messages are required for chat type"):
        ai_request(type="chat", model="test", messages=None)


def test_generate_requires_prompt():
    with pytest.raises(ValueError, match="Prompt is required for generate type"):
        ai_request(type="generate", model="test", prompt=None)
