import json
from io import BytesIO

from shadow_xai.llm import EchoAdapter, LLMMessage, LLMResponse, OpenAICompatibleAdapter


def test_echo_adapter_is_deterministic_and_local() -> None:
    result = EchoAdapter().complete([LLMMessage("user", "Halo")])
    assert "mode lokal" in result
    assert "Halo" in result


def test_model_selection_profiles() -> None:
    assert OpenAICompatibleAdapter.resolve_model("", "fast") == "gpt-5-mini"
    assert OpenAICompatibleAdapter.resolve_model("", "balanced") == "gpt-5"
    assert OpenAICompatibleAdapter.resolve_model("", "quality") == "gpt-5.5"
    assert OpenAICompatibleAdapter.resolve_model("custom-model", "quality") == "custom-model"


def test_payload_uses_family_specific_reasoning_parameters() -> None:
    messages = [LLMMessage("system", "Be helpful"), LLMMessage("user", "Hello")]
    gpt = OpenAICompatibleAdapter.build_payload(messages, model="gpt-5", reasoning_effort="high", max_output_tokens=1200)
    claude = OpenAICompatibleAdapter.build_payload(messages, model="claude-sonnet-4-6", max_output_tokens=1200)
    gemini = OpenAICompatibleAdapter.build_payload(messages, model="gemini-3-flash-preview", max_output_tokens=1200)
    assert gpt["max_completion_tokens"] == 1200
    assert gpt["reasoning"] == {"effort": "high"}
    assert "max_completion_tokens" not in claude
    assert claude["thinking"]["budget_tokens"] > 0
    assert "max_completion_tokens" not in gemini
    assert gemini["max_tokens"] == 1200


def test_response_extracts_text_and_usage() -> None:
    data = {"model": "gpt-5", "choices": [{"message": {"content": "  Jawaban profesional.  "}, "finish_reason": "stop"}], "usage": {"total_tokens": 9}}
    adapter = object.__new__(OpenAICompatibleAdapter)
    adapter.model = "gpt-5"
    adapter._request = lambda payload: data  # type: ignore[method-assign]
    response = adapter.complete_response([LLMMessage("user", "Tes")])
    assert isinstance(response, LLMResponse)
    assert response.text == "Jawaban profesional."
    assert response.usage["total_tokens"] == 9
