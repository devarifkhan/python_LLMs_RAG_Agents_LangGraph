"""
Weather Agent

1. The LLM detects whether the user is asking about the weather and extracts the city.
2. If it is a weather question, the Meteosource API is called:
     find_places  -> place_id
     point        -> current weather (sections=current, units=metric)
3. The real weather data is passed back to the LLM, which streams a final answer.
4. Non-weather questions go through a START -> PLAN -> OUTPUT reasoning chain.

All LLM responses are JSON. They are streamed to the terminal, stripped of
markdown code fences and validated with Pydantic.
"""

import os
import json
from typing import Optional

import requests
from dotenv import load_dotenv
from openai import OpenAI, OpenAIError
from pydantic import BaseModel, ValidationError

# -------------------------
# Configuration
# -------------------------
load_dotenv()
METEOSOURCE_API_KEY = os.getenv("METEOSOURCE_API_KEY")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
# When a city name matches several places, prefer one in this country (optional).
PREFERRED_COUNTRY = os.getenv("PREFERRED_COUNTRY", "Bangladesh")

MODEL = "gemini-2.5-flash"
GEMINI_OPENAI_BASE_URL = "https://generativelanguage.googleapis.com/v1beta/openai/"

METEOSOURCE_BASE_URL = "https://www.meteosource.com/api/v1/free"
REQUEST_TIMEOUT_SECONDS = 10

client: Optional[OpenAI] = None


# -------------------------
# Pydantic Models
# -------------------------
class CityInfo(BaseModel):
    weather: bool
    city: Optional[str] = None


class PlanStep(BaseModel):
    step: str
    CONTENT: str


class StepOutput(BaseModel):
    step: str
    CONTENT: str


# -------------------------
# Weather Tool (Meteosource)
# -------------------------
class WeatherError(Exception):
    """An error with a message that is safe to show to the user."""


def _meteosource_get(endpoint: str, params: dict):
    """GET a Meteosource free-tier endpoint and return the parsed JSON."""
    if not METEOSOURCE_API_KEY:
        raise WeatherError(
            "Weather service is not configured: set METEOSOURCE_API_KEY in your .env file."
        )

    url = f"{METEOSOURCE_BASE_URL}/{endpoint}"
    headers = {"X-API-Key": METEOSOURCE_API_KEY}

    try:
        response = requests.get(
            url, params=params, headers=headers, timeout=REQUEST_TIMEOUT_SECONDS
        )
    except requests.Timeout:
        raise WeatherError("The weather service took too long to respond. Please try again later.")
    except requests.RequestException as e:
        raise WeatherError(f"Could not reach the weather service ({type(e).__name__}).")

    if response.status_code in (401, 403):
        raise WeatherError("The weather service rejected the API key. Check METEOSOURCE_API_KEY.")
    if response.status_code == 429:
        raise WeatherError("Weather API rate limit reached. Please try again later.")
    if response.status_code != 200:
        raise WeatherError(f"The weather service returned an error (HTTP {response.status_code}).")

    try:
        return response.json()
    except ValueError:
        raise WeatherError("The weather service returned an invalid response.")


def find_place(city: str) -> dict:
    """Look up a city with /find_places and return the best matching place."""
    city = (city or "").strip()
    if not city:
        raise WeatherError("City name cannot be empty.")

    places = _meteosource_get("find_places", {"text": city, "language": "en"})
    if not isinstance(places, list) or not places:
        raise WeatherError(f"Could not find a city called '{city}'.")

    preferred = [p for p in places if p.get("country") == PREFERRED_COUNTRY]
    return preferred[0] if preferred else places[0]


def get_current_weather(place_id: str) -> dict:
    """Get the current weather for a place_id with the /point endpoint."""
    data = _meteosource_get(
        "point",
        {
            "place_id": place_id,
            "sections": "current",
            "units": "metric",
            "language": "en",
            "timezone": "UTC",
        },
    )
    current = data.get("current") if isinstance(data, dict) else None
    if not current:
        raise WeatherError("The weather service returned no current weather for this place.")
    return current


def getWeather(city: str) -> dict:
    """Weather tool: city name -> place info + current weather (metric units)."""
    place = find_place(city)
    place_id = place.get("place_id")
    if not place_id:
        raise WeatherError(f"Could not find a city called '{city}'.")

    current = get_current_weather(place_id)
    wind = current.get("wind") or {}

    def drop_missing(d: dict) -> dict:
        # The free tier may not return every field; don't show the LLM nulls.
        return {k: v for k, v in d.items() if v is not None}

    return {
        "place": drop_missing({
            "name": place.get("name"),
            "region": place.get("adm_area1"),
            "country": place.get("country"),
        }),
        "current": drop_missing({
            "summary": current.get("summary"),
            "temperature_c": current.get("temperature"),
            "feels_like_c": current.get("feels_like"),
            "humidity_percent": current.get("humidity"),
            "cloud_cover_percent": current.get("cloud_cover"),
            "wind_speed_m_s": wind.get("speed"),
            "wind_direction": wind.get("dir"),
            "precipitation": current.get("precipitation"),
        }),
        "units": "metric",
        "source": "Meteosource",
    }


# -------------------------
# LLM Streaming Function
# -------------------------
def strip_code_fences(text: str) -> str:
    """Remove the markdown code fences (```json ... ```) that Gemini often adds."""
    cleaned = text.strip()
    if cleaned.startswith("```"):
        cleaned = cleaned.split("\n", 1)[1] if "\n" in cleaned else cleaned[3:]
    if cleaned.endswith("```"):
        cleaned = cleaned[:-3]
    return cleaned.strip()


def ask_llm_stream(messages):
    """
    Calls the LLM with streaming and prints the output as it arrives.
    Returns the parsed JSON at the end, or a dict with an "error" key.
    """
    full_content = ""
    print()
    try:
        stream_resp = client.chat.completions.create(
            model=MODEL,
            messages=messages,
            stream=True,
        )
        for chunk in stream_resp:
            if chunk.choices and chunk.choices[0].delta.content:
                text = chunk.choices[0].delta.content
                print(text, end="", flush=True)
                full_content += text
    except OpenAIError as e:
        print(f"\nLLM request failed: {type(e).__name__}: {e}")
        return {"error": "LLM request failed", "content": full_content}
    print()

    try:
        return json.loads(strip_code_fences(full_content))
    except json.JSONDecodeError:
        return {"error": "Failed to parse JSON from streamed output", "content": full_content}


# -------------------------
# Weather answer
# -------------------------
def answer_weather_question(user_query: str, city: str):
    try:
        weather = getWeather(city)
    except WeatherError as e:
        print(f"\n⚠️  {e}")
        return

    print(f"\n🌤 Weather data for {city}:\n{json.dumps(weather, indent=2)}")

    answer_prompt = f"""
Answer the user's question using ONLY the weather data below.
Mention the place, the temperature in °C and the conditions. Include wind or
humidity if they are available. Do not invent values that are not in the data.

Weather data (JSON):
{json.dumps(weather)}

User question:
{user_query}

Return ONLY JSON.

Format:
{{"step":"OUTPUT","CONTENT":"string"}}
"""
    answer_json = ask_llm_stream([
        {"role": "system", "content": "You are a helpful weather assistant."},
        {"role": "user", "content": answer_prompt},
    ])
    try:
        answer = StepOutput(**answer_json)
        print(f"\nOUTPUT: {answer.CONTENT}")
    except (ValidationError, TypeError):
        print(f"\nOUTPUT (raw): {answer_json}")


# -------------------------
# General (non-weather) answer
# -------------------------
def answer_general_question(user_query: str):
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
    except (ValidationError, TypeError):
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
        if not isinstance(plan_res_json, list):
            raise TypeError("Expected a JSON array")
        plan_res = [PlanStep(**p) for p in plan_res_json]
        for p in plan_res:
            print(f"- {p.CONTENT}")
    except (ValidationError, TypeError):
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
    except (ValidationError, TypeError):
        print(f"\nOUTPUT (raw): {output_res_json}")


# -------------------------
# Main Agent
# -------------------------
def main():
    global client

    if not GOOGLE_API_KEY:
        print("⚠️  GOOGLE_API_KEY is not set. Add it to your .env file (see .env.example).")
        return
    client = OpenAI(api_key=GOOGLE_API_KEY, base_url=GEMINI_OPENAI_BASE_URL)

    user_query = input("👉 ").strip()
    if not user_query:
        print("Please type a question.")
        return

    # Step 0: intent detection: is this a weather question, and for which city?
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

    if isinstance(city_info_json, dict) and city_info_json.get("error") == "LLM request failed":
        print("⚠️  Could not reach the LLM. Check GOOGLE_API_KEY and your connection.")
        return

    try:
        city_info = CityInfo(**city_info_json)
    except (ValidationError, TypeError) as e:
        print(f"Failed to parse city info: {e}")
        city_info = CityInfo(weather=False, city=None)

    if city_info.weather:
        if not city_info.city:
            print("\n⚠️  Which city do you want the weather for? Please include a city name.")
            return
        answer_weather_question(user_query, city_info.city)
        return

    answer_general_question(user_query)


if __name__ == "__main__":
    main()
