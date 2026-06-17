import os
import json
import httpx

SYSTEM_PROMPT = """You are an expert social media ghostwriter.
Given source content, produce posts tailored per platform.
Respond ONLY with valid JSON in this exact shape:
{"linkedin": "...", "x_thread": ["tweet1", "tweet2", "tweet3"], "instagram": "..."}
Rules:
- linkedin: 150-250 words, hook first line, line breaks, no hashtags spam (max 3)
- x_thread: 3-5 tweets, each under 280 chars, first tweet is a strong hook
- instagram: caption with hook, value, CTA, 5 relevant hashtags at the end"""

async def generate_posts(content: str) -> dict:
    async with httpx.AsyncClient(timeout=60) as client:
        resp = await client.post(
            f"{os.environ['LLM_BASE_URL']}/chat/completions",
            headers={"Authorization": f"Bearer {os.environ['LLM_API_KEY']}"},
            json={
                "model": os.environ["LLM_MODEL"],
                "messages": [
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": content[:12000]},
                ],
                "temperature": 0.7,
                "response_format": {"type": "json_object"},
            },
        )
        resp.raise_for_status()
        return json.loads(resp.json()["choices"][0]["message"]["content"])
