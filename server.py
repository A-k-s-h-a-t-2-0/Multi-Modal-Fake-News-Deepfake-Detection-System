from __future__ import annotations

import io
import base64
from typing import List, Optional
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from PIL import Image

from src.multimodal_detector import MultiModalFakeNewsDetector
from src.schemas import NewsInput

app = FastAPI(
    title="Multi-Modal Fake News & Deepfake Detection API",
    description="Backend API exposing the weighted late-fusion misinformation classification pipeline.",
    version="1.0.0"
)

# Enable CORS for React frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize ML Fusion Detector
detector = MultiModalFakeNewsDetector()

# Pydantic schemas for request validation
class AnalyzeRequest(BaseModel):
    headline: str
    article: str
    source: str
    claim: str
    evidence: List[str]
    image_base64: Optional[str] = None

@app.post("/analyze")
def analyze_content(req: AnalyzeRequest):
    """
    Runs the late-fusion pipeline across text credibility, source reliability,
    claim alignment, and optionally image manipulation.
    """
    image = None
    if req.image_base64:
        try:
            # Strip header if it contains metadata (e.g. data:image/png;base64,...)
            img_data = req.image_base64
            if "," in img_data:
                img_data = img_data.split(",")[1]
            img_bytes = base64.b64decode(img_data)
            image = Image.open(io.BytesIO(img_bytes)).convert("RGB")
        except Exception as e:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid image file format or failed base64 decoding: {str(e)}"
            )

    try:
        result = detector.predict(
            NewsInput(
                headline=req.headline,
                article=req.article,
                source=req.source,
                claim=req.claim,
                evidence=req.evidence,
                image=image
            )
        )
        return result.to_dict()
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error running late fusion model pipeline: {str(e)}"
        )

@app.get("/health")
def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=4000)
