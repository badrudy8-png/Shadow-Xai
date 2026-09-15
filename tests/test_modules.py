from shadow_xai.agent import Agent
from shadow_xai.evaluation import EvaluationCase, evaluate
from shadow_xai.memory import MemoryStore
from shadow_xai.rag import KnowledgeBase
from shadow_xai.security import SecurityPolicy
from shadow_xai.tools import default_registry
from shadow_xai.api import APIHandler


def test_memory_export_and_delete() -> None:
    store = MemoryStore()
    store.add("u1", "user", "remember this")
    assert "remember this" in store.export_user("u1")
    store.delete_user("u1")
    assert store.recent("u1") == []


def test_calculator_allowlist_and_audit() -> None:
    tools = default_registry()
    assert tools.call("calculator", "2 + 3 * 4") == "14"
    assert tools.audit[-1]["status"] == "ok"


def test_rag_tracks_sources() -> None:
    kb = KnowledgeBase(chunk_size=3)
    kb.ingest("Shadow Xai modular engine", "guide.md")
    assert "guide.md" in kb.context("modular engine")


def test_agent_and_evaluation() -> None:
    result = Agent().run("ship feature")
    assert result.completed
    cases = [EvaluationCase("hi", ("hi",))]
    assert evaluate(cases, lambda prompt: prompt)[0].passed


def test_security_redacts_secrets() -> None:
    assert "[REDACTED]" in SecurityPolicy.redact_secrets("api_key=secret")


def test_api_handler_has_routes() -> None:
    assert callable(APIHandler.do_GET)
    assert callable(APIHandler.do_POST)
