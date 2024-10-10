from huggingface_hub import InferenceClient
import os
from dotenv import load_dotenv

load_dotenv()
hf_token = os.getenv("API_KEY")

# Hugging Face API setup for LLM
repo_id = "meta-llama/Meta-Llama-3-70B-Instruct"
llm_client = InferenceClient(model=repo_id, timeout=180, token=hf_token)

# Prompt to generate an itinerary
def generate_key_itinerary_points(text):
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

    return llm_client.text_generation(prompt, max_new_tokens=5000, stream=True, stop_sequences=["I hope that helps!"])

# Prompt to generate a list of flights
def generate_key_airplane_points(text):
    prompt = f"""                       
    Based on the following trip description: {text}, generate a list of direct flights (no layovers) as a JSON array, where each object represents one flight. 
    Each flight must contain the following information:
    - The 'departure_city' and 'arrival_city', both specified as "City, Country" format, and the corresponding IATA airport codes in parentheses.
      For example, "departure_city": "Los Angeles, USA (LAX)", "arrival_city": "Paris, France (CDG)".
    - The 'departure_date' in 'YYYY-MM-DD' format. If no date is provided in the description, use the January 15th, 2025.
    - The 'departure_time' and 'arrival_time', represented in 24-hour format, like "14:30" for 2:30 PM.
    - The 'airline' operating the flight, represented by its full name (e.g., "Delta Air Lines").
    - The 'flight_price' in USD as a numeric value without commas or currency symbols (e.g., 350.00).
    Only generate two sections: 'Thought:' provides your rationale for generating the points, then you list the locations in 'Flight suggestions:'. Then generate 'I hope that helps!' 
    to indicate the end of the response.
    Now begin.
    Description: {text}
    Thought:
    """
    return llm_client.text_generation(prompt, max_new_tokens=5000, stream=True, stop_sequences=["I hope that helps!"])

