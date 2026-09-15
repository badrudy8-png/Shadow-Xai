from io import StringIO

import pytest

from shadow_xai import ChatEngine, ChatResponse


def test_engine_returns_response_and_history() -> None:
    engine = ChatEngine()
    response = engine.respond("Halo")
    assert isinstance(response, ChatResponse)
    assert "Halo" in response.text
    assert response.provider == "echo"
    assert response.model == "echo"
    assert response.route == "default"
    assert [item.role for item in engine.history] == ["user", "assistant"]


def test_engine_rejects_empty_message() -> None:
    with pytest.raises(ValueError, match="must not be empty"):
        ChatEngine().respond("  ")


def test_router_and_agent_metadata_are_integrated() -> None:
    engine = ChatEngine()
    response = engine.respond("calculate 2 + 3")
    assert response.route == "calculator"
    assert response.agent_completed


def test_research_route_is_integrated() -> None:
    engine = ChatEngine()
    response = engine.respond("cari source tentang Shadow-Xai")
    assert response.route == "research"
    assert response.agent_completed


def test_interactive_mode_supports_help_and_exit() -> None:
    engine = ChatEngine()
    output = StringIO()
    engine.run_interactive(StringIO("/help\nHalo\n/exit\n"), output)
    text = output.getvalue()
    assert "Perintah: /help" in text
    assert "Halo" in text
    assert "Sampai jumpa." in text


def test_clear_command_removes_history() -> None:
    engine = ChatEngine()
    output = StringIO()
    engine.run_interactive(StringIO("Halo\n/clear\n/exit\n"), output)
    assert engine.history == ()
    assert "Riwayat percakapan dihapus." in output.getvalue()
