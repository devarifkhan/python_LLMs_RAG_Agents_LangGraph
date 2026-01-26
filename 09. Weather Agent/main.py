import os
import json
import requests
from dotenv import load_dotenv
from openai import OpenAI
from pydantic import BaseModel, ValidationError
from typing import List, Optional

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

# -------------------------
# Pydantic Models
# -------------------------
class CityInfo(BaseModel):
    weather: bool
    city: Optional[str]

class PlanStep(BaseModel):
    step: str
    CONTENT: str

class StepOutput(BaseModel):
    step: str
    CONTENT: str

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
        return bangladesh_places[0]

    # If no Bangladesh match, return first place
    return places[0] if places else None

# -------------------------
# LLM Streaming Function
# -------------------------
def ask_llm_stream(messages):
    """
    Calls the LLM with streaming and prints output line by line.
    Returns the full accumulated JSON at the end.
    """
    full_content = ""
    stream_resp = client.chat.completions.stream(
        model=MODEL,
        messages=messages
    )
    
    print()  # newline for clarity
    for event in stream_resp:
        if event.type == "response.output_text.delta":
            text = event.delta
            print(text, end="", flush=True)
            full_content += text
    
    print()  # final newline

    try:
        return json.loads(full_content)
    except json.JSONDecodeError:
        return {"error": "Failed to parse JSON from streamed output", "content": full_content}

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
    city_info_json = ask_llm_stream([
        {"role": "system", "content": "You detect weather queries and extract the city."},
        {"role": "user", "content": city_extraction_prompt},
    ])

    # Validate with Pydantic
    try:
        city_info = CityInfo(**city_info_json)
    except ValidationError as e:
        print(f"Failed to parse city info: {e}")
        city_info = CityInfo(weather=False, city=None)

    # -------------------------
    # If weather intent detected, call tool
    # -------------------------
    if city_info.weather and city_info.city:
        city = city_info.city
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
    start_res_json = ask_llm_stream([
        {"role": "system", "content": "You structure user input."},
        {"role": "user", "content": start_prompt},
    ])
    try:
        start_res = StepOutput(**start_res_json)
        print(f"\nSTART: {start_res.CONTENT}")
    except ValidationError:
        print(f"\nSTART (raw): {start_res_json}")

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
]
"""
    plan_res_json = ask_llm_stream([
        {"role": "system", "content": "You plan solutions step by step."},
        {"role": "user", "content": plan_prompt},
    ])
    print("\nPLAN:")
    try:
        plan_res = [PlanStep(**p) for p in plan_res_json]
        for p in plan_res:
            print(f"- {p.CONTENT}")
    except ValidationError:
        print(plan_res_json)

    # OUTPUT
    output_prompt = f"""
Solve the problem completely now:

{user_query}

Return ONLY JSON.

Format:
{{"step":"OUTPUT","CONTENT":"string"}}
"""
    output_res_json = ask_llm_stream([
        {"role": "system", "content": "You solve problems accurately."},
        {"role": "user", "content": output_prompt},
    ])
    try:
        output_res = StepOutput(**output_res_json)
        print(f"\nOUTPUT: {output_res.CONTENT}")
    except ValidationError:
        print(f"\nOUTPUT (raw): {output_res_json}")

if __name__ == "__main__":
    main()
