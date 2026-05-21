import openai
from app.config import Config

openai.api_key = Config.OPENAI_API_KEY


class PromptEnhancer:
    @staticmethod
    async def enhance_prompt(brief: str, style: str) -> str:
        """Enhance user prompt for better image generation"""

        style_guidelines = Config.STYLE_PROMPTS.get(style, "")

        system_prompt = f"""
        You are an expert prompt engineer for AI image generation (DALL-E 3, Stable Diffusion).
        Transform simple user descriptions into detailed, professional image prompts.
        
        Current style: {style_guidelines if style_guidelines else 'General purpose'}
        
        Enhance the prompt with:
        - Specific lighting details (cinematic, golden hour, dramatic)
        - Quality indicators (8k, ultra HD, photorealistic)
        - Composition and angles
        - Color palette suggestions
        - Mood and atmosphere
        - Technical photography terms
        
        Return ONLY the enhanced prompt, no explanations or extra text.
        Keep it under 300 words.
        """

        try:
            response = await openai.ChatCompletion.acreate(
                model="gpt-4-turbo-preview",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": f"Enhance this prompt: {brief}"},
                ],
                temperature=0.7,
                max_tokens=250,
            )

            enhanced = response.choices[0].message.content.strip()

        except Exception as e:
            # Fallback enhancement
            enhanced = f"Professional, high-quality advertisement image of {brief}, cinematic lighting, 8k resolution, photorealistic, detailed, vibrant colors, sharp focus, commercial photography style"

        return enhanced
