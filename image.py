import requests
import os
import base64

STABILITY_API_KEY = os.environ.get("STABILITY_API_KEY")

def generate_image(topic):
    prompt = f"professional business illustration about {topic}, corporate style, digital marketing concept, vibrant colors, no people, social media post style, high quality, 4k"

    print("🎨 Image generate হচ্ছে...")

    response = requests.post(
        "https://api.stability.ai/v1/generation/stable-diffusion-xl-1024-v1-0/text-to-image",
        headers={
            "Authorization": f"Bearer {STABILITY_API_KEY}",
            "Content-Type": "application/json",
            "Accept": "application/json"
        },
        json={
            "text_prompts": [{"text": prompt, "weight": 1}],
            "cfg_scale": 7,
            "height": 1024,
            "width": 1024,
            "samples": 1,
            "steps": 30,
        },
        timeout=60
    )

    if response.status_code == 200:
        data = response.json()
        image_data = base64.b64decode(data["artifacts"][0]["base64"])
        image_path = "generated_image.jpg"
        with open(image_path, "wb") as f:
            f.write(image_data)
        print("✅ Image তৈরি হয়েছে!")
        return image_path
    else:
        print(f"❌ Error: {response.status_code} - {response.text}")
        return None
