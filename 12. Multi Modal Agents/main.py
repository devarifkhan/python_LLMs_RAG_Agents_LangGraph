# WORK IN PROGRESS
# This multimodal (text + image) example is not finished and does not run as-is:
# the model name and the image URL below are placeholders.
# See the root README for the status of every folder.

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI()

response=client.chat.completions.create(
    model="gpt-4o-multimodal-preview",
    messages=[
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": "What is in this image?",
                },
                {
                    "type": "image_url",
                    "image_url": {
                        "url": "https://example.com/path/to/your/image.jpg"
                    },
                },
            ],
        }
    ],)

print(response.choices[0].message.content)