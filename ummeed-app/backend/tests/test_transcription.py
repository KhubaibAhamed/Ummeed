from app.services.transcription import parse_sarvam_response


def test_parses_transcript_and_language_code():
    raw = {
        "request_id": "20260829_abc123",
        "transcript": "నా పత్తి ఆకులు పసుపు రంగులో ఉన్నాయి",
        "language_code": "te-IN",
    }

    result = parse_sarvam_response(raw)

    assert result["text"] == "నా పత్తి ఆకులు పసుపు రంగులో ఉన్నాయి"
    assert result["detected_language"] == "te-IN"


def test_handles_null_language_code_when_undetected():
    raw = {"request_id": "abc", "transcript": "unclear audio", "language_code": None}

    result = parse_sarvam_response(raw)

    assert result["detected_language"] == "unknown"
