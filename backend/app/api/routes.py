from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
import asyncio
import uuid
from datetime import datetime

from app.models.job import GenerateRequest, GenerateResponse
from app.services.llm_service import LLMService
from app.services.image_service import ImageService
from app.services.prompt_enhancer import PromptEnhancer

router = APIRouter()

# In-memory job storage (replace with Redis/DB for production)
jobs = {}


@router.post("/api/generate")
async def generate_ad(request: GenerateRequest):
    """Generate ad image and copy - synchronous for demo"""

    try:
        # Step 1: Enhance prompt
        enhanced_prompt = await PromptEnhancer.enhance_prompt(
            request.prompt, request.style
        )

        # Step 2: Generate marketing copy
        marketing_copy = await LLMService.generate_marketing_copy(
            request.prompt, request.style
        )

        # Step 3: Generate image
        image_url = await ImageService.generate_image(enhanced_prompt)

        return JSONResponse(
            content={
                "success": True,
                "image_url": image_url,
                "marketing_copy": marketing_copy.get("formatted", ""),
                "enhanced_prompt": enhanced_prompt,
                "original_prompt": request.prompt,
                "style": request.style,
            }
        )

    except Exception as e:
        return JSONResponse(
            status_code=500, content={"success": False, "error": str(e)}
        )


@router.get("/api/health")
async def health_check():
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}
