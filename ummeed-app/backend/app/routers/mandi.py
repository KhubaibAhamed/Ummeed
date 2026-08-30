from fastapi import APIRouter, Depends, HTTPException

from app.dependencies import get_mandi_provider
from app.models.schemas import MandiPriceResponse

router = APIRouter()


@router.get("/mandi-price", response_model=MandiPriceResponse)
def get_mandi_price(crop: str, location: str, mandi_provider=Depends(get_mandi_provider)):
    try:
        return mandi_provider.get_price(crop, location)
    except ValueError:
        raise HTTPException(
            status_code=404, detail=f"No mandi price data found for {crop} in {location}"
        )
