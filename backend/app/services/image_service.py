import io
import base64
import httpx
import asyncio
from PIL import Image, ImageDraw, ImageFont
from app.config import Config


class ImageService:
    @staticmethod
    async def generate_image(prompt: str) -> str:
        """Generate image using Stability AI or fallback to local generation"""

        # Try Stability AI
        if (
            Config.STABILITY_API_KEY
            and Config.STABILITY_API_KEY != "your_stability_api_key_here"
        ):
            try:
                async with httpx.AsyncClient(timeout=90.0) as client:
                    response = await client.post(
                        "https://api.stability.ai/v1/generation/stable-diffusion-xl-1024-v1-0/text-to-image",
                        headers={
                            "Authorization": f"Bearer {Config.STABILITY_API_KEY}",
                            "Content-Type": "application/json",
                        },
                        json={
                            "text_prompts": [{"text": prompt, "weight": 1}],
                            "cfg_scale": 7,
                            "height": Config.IMAGE_HEIGHT,
                            "width": Config.IMAGE_WIDTH,
                            "samples": 1,
                            "steps": 40,
                        },
                    )

                    if response.status_code == 200:
                        data = response.json()
                        image_data = data["artifacts"][0]["base64"]
                        return f"data:image/png;base64,{image_data}"
            except Exception as e:
                print(f"Stability AI error: {e}")

        # Fallback to DALL-E if API key available
        if Config.OPENAI_API_KEY:
            try:
                import openai

                openai.api_key = Config.OPENAI_API_KEY

                response = await openai.Image.acreate(
                    model="dall-e-3",
                    prompt=prompt,
                    size="1024x1024",
                    quality="standard",
                    n=1,
                )

                image_url = response.data[0].url

                # Download and convert to base64 for frontend
                async with httpx.AsyncClient() as client:
                    img_response = await client.get(image_url)
                    img_base64 = base64.b64encode(img_response.content).decode()
                    return f"data:image/png;base64,{img_base64}"

            except Exception as e:
                print(f"DALL-E error: {e}")

        # Final fallback: generate placeholder with text
        return await ImageService._generate_placeholder(prompt)

    @staticmethod
    async def _generate_placeholder(prompt: str) -> str:
        """Generate a professional-looking placeholder image"""

        img = Image.new(
            "RGB", (Config.IMAGE_WIDTH, Config.IMAGE_HEIGHT), color=(30, 30, 50)
        )
        draw = ImageDraw.Draw(img)

        # Draw gradient-like effect
        for i in range(Config.IMAGE_HEIGHT):
            color_value = int(30 + (i / Config.IMAGE_HEIGHT) * 50)
            draw.line(
                [(0, i), (Config.IMAGE_WIDTH, i)],
                fill=(color_value, color_value, color_value + 20),
            )

        # Draw border
        for i in range(3):
            draw.rectangle(
                [i, i, Config.IMAGE_WIDTH - i - 1, Config.IMAGE_HEIGHT - i - 1],
                outline=(100, 100, 150),
            )

        # Add text
        try:
            font = ImageFont.truetype(
                "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 36
            )
            font_small = ImageFont.truetype(
                "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 20
            )
        except:
            font = ImageFont.load_default()
            font_small = ImageFont.load_default()

        # Center text
        lines = (
            prompt.split("\n")
            if "\n" in prompt
            else [prompt[i : i + 40] for i in range(0, len(prompt), 40)]
        )
        y = Config.IMAGE_HEIGHT // 2 - 50

        for line in lines[:3]:
            bbox = draw.textbbox((0, 0), line[:50], font=font)
            text_width = bbox[2] - bbox[0]
            x = (Config.IMAGE_WIDTH - text_width) // 2
            draw.text((x, y), line[:50], fill=(255, 255, 255), font=font)
            y += 45

        
        watermark = "AI Generated • ViralGen AI"
        bbox = draw.textbbox((0, 0), watermark, font=font_small)
        text_width = bbox[2] - bbox[0]
        draw.text(
            ((Config.IMAGE_WIDTH - text_width) // 2, Config.IMAGE_HEIGHT - 50),
            watermark,
            fill=(150, 150, 180),
            font=font_small,
        )

        
        buffered = io.BytesIO()
        img.save(buffered, format="PNG")
        img_base64 = base64.b64encode(buffered.getvalue()).decode()

        return f"data:image/png;base64,{img_base64}"
