from celery_app import celery_app
from app.services.llm_service import LLMService
from app.services.image_service import ImageGenerationService
from app.services.prompt_enhancer import PromptEnhancer
from app.services.compositor import ImageCompositor
from app.config import Config
import pymongo

# MongoDB connection
mongo_client = pymongo.MongoClient(Config.MONGODB_URL)
db = mongo_client[Config.DATABASE_NAME]
jobs_collection = db["jobs"]


@celery_app.task
def generate_social_media_asset(job_id: str):
    try:
        # Update job to processing
        jobs_collection.update_one(
            {"job_id": job_id}, {"$set": {"status": "processing"}}
        )

        job = jobs_collection.find_one({"job_id": job_id})

        brief = job["brief"]
        persona = job["persona"]
        platform = job["platform"]
        style = job.get("image_style")

        # Initialize services
        llm = LLMService()
        image_service = ImageGenerationService()
        enhancer = PromptEnhancer()
        compositor = ImageCompositor()

        # 1. Generate marketing copy
        marketing_copy = llm.generate_marketing_copy(brief, persona, platform)

        # 2. Enhance prompt
        enhanced_prompt = enhancer.enhance_prompt(brief, style)

        # 3. Generate image
        image_bytes = image_service.generate_image(enhanced_prompt)

        # 4. Compose final image
        final_path = compositor.compose_asset(image_bytes, marketing_copy, platform)

        # 5. Update job as completed
        jobs_collection.update_one(
            {"job_id": job_id},
            {
                "$set": {
                    "status": "completed",
                    "marketing_copy": marketing_copy,
                    "enhanced_prompt": enhanced_prompt,
                    "final_asset_url": final_path,
                    "image_url": final_path,
                }
            },
        )

    except Exception as e:
        jobs_collection.update_one(
            {"job_id": job_id}, {"$set": {"status": "failed", "error_message": str(e)}}
        )
