from openai import OpenAI
from dotenv import load_dotenv
import os
import requests

load_dotenv()

api_key = os.getenv("GOOGLE_API_KEY")
client = OpenAI(
    api_key=api_key, 
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"

)

BASE_URL = "https://www.meteosource.com/api/v1/free"
API_KEY = os.getenv("WEATHER_API_KEY")  # store your API key in an env variable

def getWeather(city: str):
    """
    Fetch place information for a given city name using Meteosource /find_places endpoint.
    API key is taken from environment variable WEATHER_API_KEY.
    """
    if not API_KEY:
        raise ValueError("API key not found. Set WEATHER_API_KEY environment variable.")

    if not city.strip():
        raise ValueError("City name cannot be empty")

    url = f"{BASE_URL}/find_places"
    params = {
        "text": city.strip(),
        "language": "en",  # free tier only supports English
        "key": API_KEY
    }

    response = requests.get(url, params=params, timeout=10)
    
    if response.status_code != 200:
        return {"error": response.json()}

    return response.json()


def main():
    user_query = input("Ask a weather-related question: ")
    response = client.chat.completions.create(
        model="gemini-2.5-flash",
        messages=[
            {"role": "system", "content": "You are a helpful weather agent."},
            {"role": "user", "content": user_query}
        ]
    )
    
    print("Response:", response.choices[0].message.content)

if __name__ == "__main__":
    print(getWeather("Dhaka"))