#from llama_cpp import Llama

# Define a function that uses the local model to generate trip planning suggestions
def get_trip_planning_suggestions(text):

    # Load the GGUF model
    llm = Llama(model_path="Phi-3-mini-4k-instruct-q4.gguf")

    prompt = f"""
    Only create a simple travel plan in bullet points for a "{text}" trip separated by days.
    Include a short name for anywhere between 1 to 3 ACTIVITIES and LOCATIONS per day, DO NOT INCLUDE long descriptions and focus on natural language.
    DO NOT generate an output format. Once all days are planned generate 'I hope that helps!'.
    """

    # Generate a response using the local model
    response = llm(prompt, max_tokens=2000, stream=True, stop=["I hope that helps!"])
    generated_text = ""

    for chunk in response:
        # Extract the text from each streamed chunk
        token_text = chunk['choices'][0]['text']
        generated_text += token_text
        print(token_text, end='', flush=True)  # Actively print as it's generated

    return generated_text

