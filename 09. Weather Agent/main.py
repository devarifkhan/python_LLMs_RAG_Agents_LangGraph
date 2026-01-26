import os
import json
import requests
from dotenv import load_dotenv
from openai import OpenAI

# -------------------------
# Load environment variables
# -------------------------
load_dotenv()
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

if not WEATHER_API_KEY:
    raise ValueError("Set WEATHER_API_KEY in environment variables.")
if not GOOGLE_API_KEY:
    raise ValueError("Set GOOGLE_API_KEY in environment variables.")

# -------------------------
# LLM Client
# -------------------------
client = OpenAI(
    api_key=GOOGLE_API_KEY,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)
MODEL = "gemini-2.5-flash"


def ask_llm(messages):
    """Call the LLM and return JSON object."""
    response = client.chat.completions.create(
        model=MODEL,
        response_format={"type": "json_object"},
        messages=messages,
    )
    return json.loads(response.choices[0].message.content)


# -------------------------
# Weather Tool
# -------------------------
BASE_URL = "https://www.meteosource.com/api/v1/free"


def getWeather(city: str):
    """
    Fetch place information for a given city name using Meteosource /find_places endpoint.
    Automatically selects the first Bangladesh match.
    """
    if not city.strip():
        raise ValueError("City name cannot be empty")

    url = f"{BASE_URL}/find_places"
    params = {"text": city.strip(), "language": "en", "key": WEATHER_API_KEY}

    response = requests.get(url, params=params, timeout=10)
    response.raise_for_status()
    places = response.json()

    # Filter for Bangladesh first
    bangladesh_places = [p for p in places if p["country"] == "Bangladesh"]
    if bangladesh_places:
        return bangladesh_places[0]  # first match in Bangladesh

    # If no Bangladesh match, return first place
    return places[0] if places else None


# -------------------------
# Main Agent Loop
# -------------------------
def main():
    user_query = input("👉 ")

    # -------------------------
    # Step 0: Ask LLM to extract city if weather-related
    # -------------------------
    city_extraction_prompt = f"""
        Detect if the user wants weather information.
        If yes, extract the city name.
        Return JSON ONLY:

        Format:
        {{"weather": true/false, "city": "CityName or null"}}

        User query:
        {user_query}
        """
    city_info = ask_llm(
        [
            {
                "role": "system",
                "content": "You detect weather queries and extract the city.",
            },
            {"role": "user", "content": city_extraction_prompt},
        ]
    )

    # -------------------------
    # If weather intent detected, call tool
    # -------------------------
    if city_info.get("weather") and city_info.get("city"):
        city = city_info["city"]
        try:
            weather_info = getWeather(city)
            print(f"\n🌤 Weather info for {city}:\n{json.dumps(weather_info, indent=2)}")
        except Exception as e:
            print(f"Error fetching weather: {e}")
        return  # exit after weather tool

    # -------------------------
    # Otherwise, handle general queries
    # -------------------------
    # START
    start_prompt = f"""
        Return ONLY JSON.

        Format:
        {{"step":"START","CONTENT":"string"}}

        User query:
        {user_query}
        """
    start_res = ask_llm(
        [
            {"role": "system", "content": "You structure user input."},
            {"role": "user", "content": start_prompt},
        ]
    )
    print(f"\nSTART: {start_res['CONTENT']}")

    # PLAN
    plan_prompt = f"""
        You are solving the following problem:

        {user_query}

        Break the solution into clear logical steps.
        Do NOT solve it yet.

        Return ONLY JSON ARRAY.

        Format:
        [
        {{"step":"PLAN","CONTENT":"string"}}
        ]"""
    plan_res = ask_llm(
        [
            {"role": "system", "content": "You plan solutions step by step."},
            {"role": "user", "content": plan_prompt},
        ]
    )
    print("\nPLAN:")
    for p in plan_res:
        print(f"- {p['CONTENT']}")

    # OUTPUT
    output_prompt = f"""
        Solve the problem completely now:

        {user_query}

        Return ONLY JSON.

        Format:
        {{"step":"OUTPUT","CONTENT":"string"}}
        """
    output_res = ask_llm(
        [
            {"role": "system", "content": "You solve problems accurately."},
            {"role": "user", "content": output_prompt},
        ]
    )
    print(f"\nOUTPUT: {output_res['CONTENT']}")


if __name__ == "__main__":
    main()
