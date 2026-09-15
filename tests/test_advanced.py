import time

from shadow_xai.advanced import BackgroundJobRegistry, ConversationSummarizer, FactChecker, IntelligentRouter, KnowledgeGraph, ParallelToolExecutor


def test_summarizer_and_fact_checker() -> None:
    assert ConversationSummarizer().summarize(["one", "two"]) == "one two"
    result = FactChecker().check("Shadow Xai engine", [("guide", "Shadow Xai has an engine")])
    assert result.supported and result.sources == ("guide",)


def test_router_parallel_and_graph() -> None:
    router = IntelligentRouter({"default": lambda _: "ok", "calculator": lambda _: "math"})
    assert router.dispatch("hitung 1+1") == "math"
    executor = ParallelToolExecutor(2)
    assert sorted(executor.run([(lambda x: x, ("a",), {}), (lambda x: x, ("b",), {})])) == ["a", "b"]
    executor.close()
    graph = KnowledgeGraph(); graph.add("Shadow", "has", "Engine")
    assert ("has", "Engine") in graph.neighbors("Shadow")


def test_background_job() -> None:
    jobs = BackgroundJobRegistry()
    job_id = jobs.submit(lambda: "done")
    for _ in range(20):
        if jobs.get(job_id).status == "completed": break
        time.sleep(0.01)
    assert jobs.get(job_id).result == "done"
