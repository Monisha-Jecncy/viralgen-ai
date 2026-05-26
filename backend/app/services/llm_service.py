import openai
import json
from app.config import Config

openai.api_key = Config.OPENAI_API_KEY


class LLMService:
    @staticmethod
    async def generate_marketing_copy(prompt: str, style: str) -> dict:
        """Generate marketing copy using GPT-4 Turbo"""

        style_guidelines = Config.STYLE_PROMPTS.get(
            style, Config.STYLE_PROMPTS["professional"]
        )

        system_prompt = f"""
        You are an expert广告文案撰写人。根据以下风格指南生成营销文案：
        
        风格指南：{style_guidelines}
        
        要求：
        1. 生成一个吸引人的标题
        2. 生成3-5句描述正文
        3. 生成5-10个相关标签
        4. 添加行动号召（CTA）
        
        以JSON格式返回，包含以下字段：
        {{"headline": "", "body": "", "hashtags": "", "cta": ""}}
        """

        try:
            response = await openai.ChatCompletion.acreate(
                model="gpt-4-turbo-preview",  # Latest GPT-4 Turbo model
                messages=[
                    {"role": "system", "content": system_prompt},
                    {
                        "role": "user",
                        "content": f"为以下产品/服务生成广告文案：{prompt}",
                    },
                ],
                temperature=0.8,
                max_tokens=500,
            )

            content = response.choices[0].message.content
            # Clean response
            content = content.replace("```json", "").replace("```", "").strip()
            result = json.loads(content)

            
            formatted = f"""
✨ **{result.get('headline', '')}** ✨

{result.get('body', '')}

📢 {result.get('cta', '')}

{result.get('hashtags', '')}
            """

            return {"raw": result, "formatted": formatted.strip()}

        except Exception as e:
            # Fallback content
            fallback = {
                "headline": f"✨ Amazing {prompt} ✨",
                "body": f"Experience the best quality with our premium offering. Don't miss out on this opportunity!",
                "cta": "Shop Now! Limited time offer!",
                "hashtags": "#Marketing #Innovation #Quality",
            }
            formatted = f"""
✨ **{fallback['headline']}** ✨

{fallback['body']}

📢 {fallback['cta']}

{fallback['hashtags']}
            """
            return {"raw": fallback, "formatted": formatted.strip()}
