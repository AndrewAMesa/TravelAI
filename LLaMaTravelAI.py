import asyncio
from huggingface_hub import InferenceClient
from geopy.geocoders import Nominatim
from geopy.adapters import AioHTTPAdapter
from geopy.exc import GeocoderQuotaExceeded
from ast import literal_eval
import pandas as pd
import numpy as np
import time
import re
import os
from dotenv import load_dotenv

load_dotenv()

hf_token = os.getenv("API_KEY")

# Hugging Face API setup for LLM
repo_id = "meta-llama/Meta-Llama-3-70B-Instruct"
llm_client = InferenceClient(model=repo_id, timeout=180, token=hf_token)

# Function to generate key points using the LLM
def generate_key_points(text):
    prompt = f"""             
    Generate a set of key geographical points for the following description: {text}, as a json list with the number dictionaries matching the number of requested days, if
    no time is suggested make one make a dictionary with less then 10. Dictionary must include the following keys: 'name', 'description'.
    ALWAYS precise the city and country in the 'name'. For instance do not only "name": "Notre Dame" as the name but "name": "Notre Dame, Paris, France".
    Also, provide enough activities to fill **each day** of the trip, ensuring that there are distinct points for each day, such that every day of the trip is planned out.
    Consider the trip timing (morning, afternoon, evening) and whether the locations are accessible during the season specified.
    Only generate two sections: 'Thought:' provides your rationale for generating the points, then you list the locations in 'Key points:'. Then generate 'I hope that helps!' 
    to indicate the end of the response.
    Now begin.
    Description: {text}
    Thought:"""

    return llm_client.text_generation(prompt, max_new_tokens=3000, stream=True, stop_sequences=["I hope that helps!"])


# Function to parse the output from the LLM
def parse_llm_output(output):
    rationale = "Thought: " + output.split("Key points:")[0]
    key_points = output.split("Key points:")[1]
    output = key_points.replace("    ", "").replace("I hope that helps!", "").strip()
    parsed_output = literal_eval(output)
    dataframe = pd.DataFrame.from_dict(parsed_output)
    return dataframe, rationale


# Geocoding function to get coordinates
async def geocode_address(address):
    geolocator = Nominatim(user_agent="HF-trip-planner", adapter_factory=AioHTTPAdapter)
    location = await geolocator.geocode(address, timeout=10)
    if location:
        return {'lat': location.latitude, 'lon': location.longitude}
    return None


# Updated function to ensure the event loop and client sessions are handled properly
async def ageocode_addresses(addresses):
    locations = []
    async with Nominatim(user_agent="HF-trip-planner", adapter_factory=AioHTTPAdapter) as geolocator:
        for address in addresses:
            try:
                location = await geolocator.geocode(address, timeout=10)
                if location:
                    locations.append({'lat': location.latitude, 'lon': location.longitude})
                else:
                    locations.append(None)
            except GeocoderQuotaExceeded as e:
                print(f"Rate limit reached. Retrying in 2 minutes...")
                time.sleep(120)  # Wait for 2 minutes and try again
                location = await geolocator.geocode(address, timeout=10)
                if location:
                    locations.append({'lat': location.latitude, 'lon': location.longitude})
                else:
                    locations.append(None)
    return locations

def geocode_addresses(addresses):
    return asyncio.run(ageocode_addresses(addresses))

def extract_num_days_from_prompt(description):
    match = re.search(r'(\d+)\s*(day|days|week|weeks)', description.lower())
    if match:
        number = int(match.group(1))
        unit = match.group(2)
        if 'day' in unit:
            return number
        elif 'week' in unit or 'weekly' in unit:
            return number * 7
    else:
        while True:
            try:
                num_days = int(input("How many days is your trip? "))
                if num_days <= 0:
                    raise ValueError("Please enter a positive number.")
                break
            except ValueError as e:
                print(f"Invalid input: {e}. Please enter a valid number of days.")
        return num_days

def split_trip_into_days(dataframe, num_days):
    day_splits = np.array_split(dataframe.index, num_days)
    days = {f"Day {i + 1}": dataframe.loc[split] for i, split in enumerate(day_splits)}
    return days
