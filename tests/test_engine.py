import pytest

from shadow_xai import ChatEngine, ChatResponse


def test_engine_returns_response() -> None:
    response = ChatEngine().respond("Halo")
    assert isinstance(response, ChatResponse)
    assert "Halo" in response.text
    assert response.provider == "placeholder"


def test_engine_rejects_empty_message() -> None:
    with pytest.raises(ValueError, match="must not be empty"):
        ChatEngine().respond("  ")
