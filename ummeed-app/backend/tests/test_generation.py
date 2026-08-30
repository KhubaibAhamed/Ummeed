from app.services.generation import build_prompt, generate_answer


class FakeLLMProvider:
    def __init__(self, fixed_response="This is a generated answer."):
        self.calls: list[str] = []
        self._fixed_response = fixed_response

    def generate(self, prompt: str) -> str:
        self.calls.append(prompt)
        return self._fixed_response


SAMPLE_CHUNKS = [
    {
        "chunk_text": "Cercospora leaf spot appears during high humidity above 65%.",
        "document_title": "ICAR Cotton Advisory 2025",
        "document_id": "d1",
        "char_start": 0,
        "char_end": 60,
        "score": 0.87,
    }
]

SAMPLE_LIVE_DATA = [
    {"label": "Guntur weather", "value": "68% humidity, falling", "source": "OpenWeatherMap"}
]


# ---------- build_prompt ----------

def test_build_prompt_includes_grounding_instruction():
    prompt = build_prompt("Why are my leaves yellow?", "en", SAMPLE_CHUNKS, [])
    lower = prompt.lower()
    assert "only" in lower
    assert "context" in lower


def test_build_prompt_includes_chunk_text_and_source_label():
    prompt = build_prompt("Why are my leaves yellow?", "en", SAMPLE_CHUNKS, [])
    assert "Cercospora leaf spot appears during high humidity above 65%." in prompt
    assert "ICAR Cotton Advisory 2025" in prompt


def test_build_prompt_includes_live_data_labeled_as_real_time():
    prompt = build_prompt("Should I spray?", "en", SAMPLE_CHUNKS, SAMPLE_LIVE_DATA)
    assert "68% humidity, falling" in prompt
    assert "real-time" in prompt.lower() or "live" in prompt.lower()


def test_build_prompt_includes_query_and_language():
    prompt = build_prompt("Why are my leaves yellow?", "hi", SAMPLE_CHUNKS, [])
    assert "Why are my leaves yellow?" in prompt
    assert "hi" in prompt


# ---------- generate_answer ----------

def test_generate_answer_short_circuits_when_no_chunks_retrieved():
    llm = FakeLLMProvider()

    result = generate_answer(
        query="something totally unrelated to farming",
        language="en",
        retrieved_chunks=[],
        live_data=[],
        llm_provider=llm,
    )

    assert llm.calls == []  # never called the LLM — this is the anti-hallucination gate
    assert result["grounded"] is False
    assert "don't have" in result["answer"].lower() or "no reliable" in result["answer"].lower()
    assert result["citations"] == []


def test_generate_answer_calls_llm_when_chunks_present():
    llm = FakeLLMProvider(fixed_response="Remove affected leaves and monitor humidity.")

    result = generate_answer(
        query="Why are my leaves yellow?",
        language="en",
        retrieved_chunks=SAMPLE_CHUNKS,
        live_data=[],
        llm_provider=llm,
    )

    assert len(llm.calls) == 1
    assert result["answer"] == "Remove affected leaves and monitor humidity."
    assert result["grounded"] is True


def test_generate_answer_returns_citations_from_retrieved_chunks():
    llm = FakeLLMProvider()

    result = generate_answer(
        query="Why are my leaves yellow?",
        language="en",
        retrieved_chunks=SAMPLE_CHUNKS,
        live_data=[],
        llm_provider=llm,
    )

    assert result["citations"] == [
        {
            "document_title": "ICAR Cotton Advisory 2025",
            "snippet": "Cercospora leaf spot appears during high humidity above 65%.",
            "page_ref": None,
        }
    ]


def test_generate_answer_passes_through_live_data():
    llm = FakeLLMProvider()

    result = generate_answer(
        query="Should I spray?",
        language="en",
        retrieved_chunks=SAMPLE_CHUNKS,
        live_data=SAMPLE_LIVE_DATA,
        llm_provider=llm,
    )

    assert result["live_data"] == SAMPLE_LIVE_DATA
