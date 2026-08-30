from typing import Protocol

FALLBACK_MESSAGE = (
    "I don't have reliable information on that in my current sources. "
    "Please try rephrasing, or ask a local agricultural officer for this specific question."
)

SYSTEM_INSTRUCTION = (
    "You are Ummeed, a farming advisory assistant. Answer ONLY using the information "
    "given in the CONTEXT below. If the context does not fully cover the question, "
    "say so explicitly rather than guessing or adding information from general knowledge. "
    "Be concise and practical — the farmer needs an actionable answer, not an essay."
)


class LLMProvider(Protocol):
    """A Protocol so generation logic is testable without a live Gemini API call."""

    def generate(self, prompt: str) -> str: ...


def build_prompt(
    query: str, language: str, retrieved_chunks: list[dict], live_data: list[dict]
) -> str:
    """
    Builds the full prompt sent to the LLM. The grounding instruction here is the
    actual anti-hallucination mechanism from the Phase 6 design — it's an explicit
    constraint we wrote, not an inherent property of "using RAG."
    """
    sections = [SYSTEM_INSTRUCTION, "", "CONTEXT (from verified documents):"]

    for chunk in retrieved_chunks:
        sections.append(f"- [Source: {chunk['document_title']}] {chunk['chunk_text']}")

    if live_data:
        sections.append("")
        sections.append("REAL-TIME DATA (live, not from documents):")
        for item in live_data:
            sections.append(f"- {item['label']}: {item['value']} (source: {item['source']})")

    sections.append("")
    sections.append(f"Farmer's question (respond in language code '{language}'): {query}")

    return "\n".join(sections)


def generate_answer(
    query: str,
    language: str,
    retrieved_chunks: list[dict],
    live_data: list[dict],
    llm_provider: LLMProvider,
) -> dict:
    """
    Orchestrates the final answer. If retrieval found nothing confident, this
    short-circuits BEFORE calling the LLM at all — the honest "I don't know" comes
    from our own logic, not from hoping the model refuses to guess.
    """
    if not retrieved_chunks:
        return {
            "answer": FALLBACK_MESSAGE,
            "citations": [],
            "live_data": live_data,
            "grounded": False,
        }

    prompt = build_prompt(query, language, retrieved_chunks, live_data)
    answer_text = llm_provider.generate(prompt)

    citations = [
        {
            "document_title": chunk["document_title"],
            "snippet": chunk["chunk_text"],
            "page_ref": chunk.get("page_ref"),
        }
        for chunk in retrieved_chunks
    ]

    return {
        "answer": answer_text,
        "citations": citations,
        "live_data": live_data,
        "grounded": True,
    }


class GeminiLLMProvider:
    """
    Real implementation, wrapping Gemini for answer generation. Only constructed
    and exercised once a real GEMINI_API_KEY is configured — not used in unit tests.
    """

    def __init__(self, api_key: str, model: str = "gemini-3.6-flash"):
        if not api_key:
            raise ValueError("GEMINI_API_KEY is required to construct GeminiLLMProvider")
        self._api_key = api_key
        self._model = model
        self._client = None

    def _get_client(self):
        if self._client is None:
            from google import genai

            self._client = genai.Client(api_key=self._api_key)
        return self._client

    def generate(self, prompt: str) -> str:
        client = self._get_client()
        response = client.models.generate_content(model=self._model, contents=prompt)
        return response.text
