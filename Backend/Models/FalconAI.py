from huggingface_hub import InferenceClient
import os
from dotenv import load_dotenv

load_dotenv()
hf_token = os.getenv("API_KEY")

# Hugging Face API setup for LLM
repo_id = "tiiuae/falcon-7b-instruct"
llm_client = InferenceClient(model=repo_id, timeout=180, token=hf_token)

# Prompt to generate an itinerary
def generate_key_itinerary_points(text):
    prompt = f"""
    Only create a simple travel plan in bullet points for a "{text}" trip separated by days.
    Include a short name for anywhere between 1 to 3 ACTIVITIES and LOCATIONS per day, DO NOT INCLUDE long descriptions and focus on natural language.
    DO NOT generate an output format. Once all days are planned generate 'I hope that helps!'.             
    """

    return llm_client.text_generation(prompt, max_new_tokens=5000, stream=True, stop_sequences=["I hope that helps!"])

# Prompt to generate a list of flights
def generate_key_airplane_points(text):
    prompt = f"""                       
    Only create a list of flights from the departure city to arrival city in this text: "{text}".
    Include the airline name, price in USD, departure time, and arrival time. DO NOT INCLUDE long descriptions and FOCUS ON NATURAL LANGUAGE.
    Return text in NATURAL LANGUAGE SENTENCE and once 5 flights are generated, generate 'I hope that helps!'.
    """
    return llm_client.text_generation(prompt, max_new_tokens=5000, stream=True, stop_sequences=["I hope that helps!"])

# Prompt to generate a list of hotels in a city
def generate_key_lodging_points(text):
    prompt = f"""                       
    Only create a list of hotels for the city "{text}".
    Include a short name for the hotel and a price in USD, DO NOT INCLUDE long descriptions and focus on natural language.
    Return text in NATURAL LANGUAGE SENTENCE and once 5 hotels are generated, generate 'I hope that helps!'.
    """
    return llm_client.text_generation(prompt, max_new_tokens=5000, stream=True, stop_sequences=["I hope that helps!"])

# Prompt to generate a list of hotels in a city
def generate_generic_travel_prompt(text):
    prompt = f"""
    You are an expert travel assistant. Based on the following inquiry: "{text}", provide a detailed response with relevant travel information.
    DO NOT INCLUDE long descriptions and focus on natural language.
    Return text in NATURAL LANGUAGE SENTENCE and once you are done generate 'I hope that helps!'.
    """
    return llm_client.text_generation(prompt, max_new_tokens=3000, stream=True, stop_sequences=["I hope that helps!"])
