import requests
from config import PAGE_ID, PAGE_ACCESS_TOKEN

def publish_post(message, image_path=None):

    # Image সহ post করো
    if image_path:
        print("📸 Image সহ post করা হচ্ছে...")

        url = f"https://graph.facebook.com/{PAGE_ID}/photos"

        with open(image_path, "rb") as img:
            data = {
                "caption": message,
                "access_token": PAGE_ACCESS_TOKEN
            }
            files = {
                "source": img
            }
            res = requests.post(url, data=data, files=files)

    # শুধু text post করো
    else:
        print("📝 Text post করা হচ্ছে...")

        url = f"https://graph.facebook.com/{PAGE_ID}/feed"

        data = {
            "message": message,
            "access_token": PAGE_ACCESS_TOKEN
        }
        res = requests.post(url, data=data)

    print("Status:", res.status_code)
    print("Response:", res.text)