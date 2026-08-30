from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from slowapi import Limiter
from slowapi.util import get_remote_address

from app.routers import mandi, query, transcribe, weather

app = FastAPI(title="Ummeed API", version="0.1.0")

# Rate limiting — protects the shared demo link's free-tier API keys from being drained.
limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter

# CORS — wide open for hackathon demo; tighten to the real frontend origin before any
# public deployment beyond the demo.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health_check():
    """Basic liveness check — confirms the service is up, not that dependencies are."""
    return {"status": "ok", "service": "ummeed-api"}


# Routers get included here as Phase 8 builds each module:
app.include_router(query.router)
app.include_router(weather.router)
app.include_router(mandi.router)
app.include_router(transcribe.router)
