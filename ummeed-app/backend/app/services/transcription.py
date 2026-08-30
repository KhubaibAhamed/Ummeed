from typing import Protocol

import httpx


class TranscriptionProvider(Protocol):
    """A Protocol so /transcribe logic can be tested without a live Sarvam API call."""

    def transcribe(self, audio_bytes: bytes, filename: str) -> dict: ...


def parse_sarvam_response(raw: dict) -> dict:
    """
    Turns Sarvam's raw JSON ({"transcript": ..., "language_code": ...}) into our
    clean shape. language_code can be null when Sarvam couldn't confidently detect
    the language — we surface that as "unknown" rather than crashing on None.
    """
    return {
        "text": raw["transcript"],
        "detected_language": raw.get("language_code") or "unknown",
    }


class SarvamSTTProvider:
    """
    Real implementation, wrapping Sarvam AI's Speech-to-Text REST endpoint
    (saaras:v3, mode=transcribe). Only exercised once SARVAM_API_KEY is configured —
    not used in unit tests, which test parse_sarvam_response directly instead.
    """

    ENDPOINT = "https://api.sarvam.ai/speech-to-text"

    def __init__(self, api_key: str, timeout_seconds: float = 10.0):
        if not api_key:
            raise ValueError("SARVAM_API_KEY is required")
        self._api_key = api_key
        # Voice queries need more time than the 3s live-data timeout — real audio
        # upload + transcription genuinely takes longer than a weather API call.
        self._timeout = timeout_seconds

    def transcribe(self, audio_bytes: bytes, filename: str) -> dict:
        headers = {"api-subscription-key": self._api_key}
        files = {"file": (filename, audio_bytes)}
        data = {"model": "saaras:v3", "mode": "transcribe"}

        with httpx.Client(timeout=self._timeout) as client:
            response = client.post(self.ENDPOINT, headers=headers, files=files, data=data)
            response.raise_for_status()

        return parse_sarvam_response(response.json())
