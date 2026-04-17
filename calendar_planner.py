import json
import os
from groq import Groq

client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

def create_calendar(niche, issues=[]):
    issues_text = ", ".join(issues) if issues else "সাধারণ সমস্যা"

    prompt = f"""
তুমি একজন expert Facebook content strategist।

নিশ: {niche}
Audience এর সমস্যা: {issues_text}

৭ দিনের viral Facebook content calendar তৈরি করো।
শুধু এই JSON format এ return করো, অন্য কিছু লিখবে না:
[
  {{
    "day": 1,
    "topic": "topic এখানে",
    "tone": "tone এখানে",
    "content_type": "type এখানে"
  }}
]

Tones: Inspirational, Professional, Storytelling, Bold, Friendly, Educational, Motivational
Content Types: Educational, Motivational Story, Tips & Tricks, Problem & Solution, Case Study, Myth vs Reality, How To Guide
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=2000
    )

    text = response.choices[0].message.content.strip()

    try:
        if "```" in text:
            text = text.split("```")[1]
            if text.startswith("json"):
                text = text[4:]
        return json.loads(text.strip())
    except:
        # Fallback
        topics = [
            f"{niche} দিয়ে সফল হওয়ার ৫টি উপায়",
            f"{niche} এ নতুনদের সবচেয়ে বড় ভুল",
            f"{niche} থেকে আয় করার real story",
            f"{niche} এর future কেমন হবে?",
            f"{niche} শুরু করার complete guide",
            f"{niche} এ সফলদের secret",
            f"{niche} নিয়ে যত misconception",
        ]
        tones = ["Inspirational", "Bold", "Storytelling", "Educational", "Motivational", "Professional", "Friendly"]
        types = ["Tips & Tricks", "Problem & Solution", "Motivational Story", "Educational", "How To Guide", "Case Study", "Myth vs Reality"]
        return [{"day": i+1, "topic": t, "tone": tones[i], "content_type": types[i]} for i, t in enumerate(topics)]
