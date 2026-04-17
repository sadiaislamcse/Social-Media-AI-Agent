import random

TOPICS = [
    "Artificial Intelligence",
    "Online Income",
    "Freelancing Tips",
    "Digital Marketing",
    "Future Technology",
    "Passive Income",
    "Startup Ideas"
]

TONES = [
    "Calm",
    "Inspirational",
    "Professional",
    "Motivational",
    "Storytelling",
    "Friendly",
    "Educational",
    "Bold"
]

def plan_post():

    topic = random.choice(TOPICS)
    tone = random.choice(TONES)

    return topic, tone