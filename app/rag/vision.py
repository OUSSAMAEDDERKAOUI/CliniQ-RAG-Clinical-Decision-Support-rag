import base64
import requests
import os

OLLAMA_URL = os.getenv("OLLAMA_URL")

def describe_image(image_path):

    try:
        with open(image_path, "rb") as f:
            img_bytes = f.read()

        img_base64 = base64.b64encode(img_bytes).decode()

        payload = {
                "model": "llava",
                "stream": False,
                "messages": [
                    {
                        "role": "system",
                        "content": "Tu es un assistant expert en analyse d'images biomédicales. Tu dois toujours répondre en français."
                    },
                    {
                        "role": "user",
                        "content": "Décris précisément cette image.",
                        "images": [img_base64]
                    }
                ]
            }           


        response = requests.post(OLLAMA_URL, json=payload)
        response.raise_for_status()

        data = response.json()

        print("\n===== RAW OLLAMA RESPONSE =====")
        print(data)
        print("===============================\n")

        message = data.get("message", {})
        content = message.get("content", "")

        return content

    except Exception as e:
        return f"Erreur description image: {str(e)}"
