
# TravelAI  
An AI assistant to streamline travel planning. Use it to:  
- Plan itineraries  
- Compare flights  
- List hotels  
- Answer general travel questions  

## Table of Contents  
- [Running the Application](#running-the-application)  
- [Using a Local Model](#using-a-local-model)  
- [Getting API Keys](#getting-api-keys)  
- [Setting Up the Database](#setting-up-the-database)  
- [Necessary Imports](#necessary-imports)  

---

## Running the Application  

### Command Line  
1. Execute `MainAPP.py` from the command line and select **option 1**.  
   - If you have set up a PostgreSQL database, you can use the database features.  
   - To skip the database login, select **option 3** to continue as a guest.  
2. Choose one of the four query types to interact with the assistant.  

### User Interface  
1. Run `MainAPP.py` and select **option 2 (Flask server)**.  
2. In a new terminal, navigate to the `Frontend` directory and start the React app:  
   ```bash
   cd Frontend/frontend  
   npm start  
   ```  
3. The React app will open on your device, allowing you to interact with the application.  
   - **Note:** Login functionality is currently not available in the UI.  

---

## Using a Local Model  

1. Install the necessary package:  
   ```bash
   pip install llama-cpp-python  
   ```  
2. Download the model **Phi-3-mini-4k-instruct-q4.gguf** from [Hugging Face](https://huggingface.co/microsoft/Phi-3-mini-4k-instruct-gguf).  
3. Place the downloaded file in the root directory of the project.  

**Note:** If you prefer not to use the local model, comment out the following line in `PhiLocalAI.py`:  
```python
from llama_cpp import Llama  
```

---

## Getting API Keys  

1. To use the LLaMa or Falcon model with Hugging Face or access the Amadeus API, you need API keys.  
2. Create a `.env` file in the project’s root directory.  
3. Register for free API keys on Hugging Face and Amadeus.
   1. Note to use the LLaMa model you must have a pro Hugging Face Account. If you don't the application will default to the Falcon model.
   2. To get a Hugging Face key with pro access request access to this [document](https://docs.google.com/document/d/1w6b5YdFhWuwHhrJHQY5AdTrfeazHS6-80gX7Kkh9Foo/edit?usp=sharing). **DO NOT SHARE THIS API KEY WITH OTHERS.**
4. Add the keys to the `.env` file in the following format:  
   ```  
   API_KEY="your_huggingface_key"  
   FLIGHT_KEY="your_amadeus_key"  
   FLIGHT_SECRET="your_amadeus_secret"  
   ```  

---

## Setting Up the Database  

1. Install PostgreSQL.  
2. Create a new server with the following details:  
   - **Name:** local  
   - **Hostname:** localhost  
   - **Port:** 5432  
   - **Username:** postgres  
   - **Password:** postgres

---

## Necessary Imports  

You may need to install the following libraries to run the code:  

```bash
pip install llama-cpp-python  
pip install huggingface_hub  
pip install react  
pip install react-cors  
pip install pandas  
pip install flask  
pip install geopy  
```
