from planner import plan_post
from generator import generate_post
from publisher import publish_post
from memory import save_post

def run_agent():

    topic, tone = plan_post()

    print("📌 Topic:", topic)
    print("🎭 Tone:", tone)

    content = generate_post(topic, tone)
    print("\n✍️ Generated Post:\n")
    print(content)

    # Image generate করার চেষ্টা করো, না হলে text-only post করো
    image_path = None
    try:
        from image import generate_image
        image_path = generate_image(topic)
    except Exception as e:
        print(f"⚠️ Image error: {e} — text-only post করা হবে")

    publish_post(content, image_path)

    save_post(topic)

    print("\n✅ Posted Successfully!")


if __name__ == "__main__":
    run_agent()
