from fastapi import APIRouter, Depends, HTTPException, UploadFile

from app.dependencies import get_transcription_provider
from app.models.schemas import TranscribeResponse

router = APIRouter()


@router.post("/transcribe", response_model=TranscribeResponse)
async def transcribe(
    audio: UploadFile, transcription_provider=Depends(get_transcription_provider)
):
    audio_bytes = await audio.read()

    try:
        result = transcription_provider.transcribe(audio_bytes, audio.filename)
    except Exception:
        raise HTTPException(
            status_code=422,
            detail="Couldn't understand that audio clearly — try again or type your question.",
        )

    return result
