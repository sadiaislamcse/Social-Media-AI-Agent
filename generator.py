import os
from groq import Groq

client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

def generate_post(topic, tone, niche="", language="English"):

    lang_lower = language.lower().strip()

    if lang_lower in ["bangla", "বাংলা", "bengali", "bn"]:
        lang_instruction = """IMPORTANT: Write the ENTIRE post in Bengali/Bangla script only.
Every single word must be in Bangla. Zero English words allowed.
Start with a Bangla sentence."""
    else:
        lang_instruction = f"Write the entire post in {language} only."

    prompt = f"""You are a professional social media content writer for a business page.

Niche: {niche}
Topic: {topic}
Tone: {tone}

{lang_instruction}

Write a Facebook post for a professional business page. Style guidelines:

- 150-200 words
- Professional yet conversational — like a knowledgeable expert sharing insights
- Start with a HOOK: a surprising fact, a relatable business scenario, or a thought-provoking statement
- Include a SHORT real-world example or mini case study (1-2 sentences)
- Use storytelling to make it engaging — but keep it professional
- Vary the structure: sometimes start with data, sometimes with a question, sometimes with a story
- 3-5 emojis placed naturally
- End with a question that invites professional discussion
- 3-5 relevant hashtags on a new line

AVOID:
- Generic openers like "In today's world" or "It's no secret"
- Buzzwords like "leverage", "synergy", "utilize"
- Overly casual language (no slang)
- AI-sounding phrases

Write ONLY the post content. Nothing else."""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=500,
        temperature=0.85
    )
    return response.choices[0].message.content.strip()
