import io

from fastapi.testclient import TestClient

from app.dependencies import get_transcription_provider
from app.main import app


class FakeTranscriptionProvider:
    def transcribe(self, audio_bytes, filename):
        return {"text": "నా పత్తి ఆకులు పసుపు రంగులో ఉన్నాయి", "detected_language": "te-IN"}


class FailingTranscriptionProvider:
    def transcribe(self, audio_bytes, filename):
        raise ValueError("could not understand audio")


def test_transcribe_endpoint_returns_text_and_language():
    app.dependency_overrides[get_transcription_provider] = lambda: FakeTranscriptionProvider()
    client = TestClient(app)

    fake_audio = io.BytesIO(b"fake audio bytes")
    response = client.post(
        "/transcribe", files={"audio": ("recording.wav", fake_audio, "audio/wav")}
    )
    app.dependency_overrides.clear()

    assert response.status_code == 200
    body = response.json()
    assert body["text"] == "నా పత్తి ఆకులు పసుపు రంగులో ఉన్నాయి"
    assert body["detected_language"] == "te-IN"


def test_transcribe_endpoint_returns_422_when_provider_cannot_understand_audio():
    app.dependency_overrides[get_transcription_provider] = lambda: FailingTranscriptionProvider()
    client = TestClient(app)

    fake_audio = io.BytesIO(b"garbage")
    response = client.post(
        "/transcribe", files={"audio": ("recording.wav", fake_audio, "audio/wav")}
    )
    app.dependency_overrides.clear()

    assert response.status_code == 422


def test_transcribe_endpoint_requires_a_file():
    app.dependency_overrides[get_transcription_provider] = lambda: FakeTranscriptionProvider()
    client = TestClient(app)

    response = client.post("/transcribe")
    app.dependency_overrides.clear()

    assert response.status_code == 422
