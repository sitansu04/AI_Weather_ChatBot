from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import requests
import os
from dotenv import load_dotenv
import uvicorn
import string

# --- Optional for RAG/NLP ---
from langchain_community.vectorstores import Chroma
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
from langchain_community.llms import HuggingFaceHub


# Load environment variables
load_dotenv()
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")

app = FastAPI(
    title="🤖 AI Weather ChatBot API",
    version="2.0.0",
    description="An NLP-powered Weather Chatbot API built with FastAPI and RAG retrieval."
)

# ---------------- MODELS ---------------- #
class CityRequest(BaseModel):
    city: str

class ChatRequest(BaseModel):
    message: str

# ---------------- WEATHER FUNCTIONS ---------------- #

def clean_city_name(city: str) -> str:
    return city.strip().translate(str.maketrans('', '', string.punctuation))

def extract_city(message: str) -> str:
    words = message.lower().split()
    if "in" in words:
        city_index = words.index("in") + 1
        city = words[city_index]
        return clean_city_name(city)
    return ""


def get_weather(city: str):
    base_url = f"http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={WEATHER_API_KEY}&units=metric"
    params = {"q": city, "appid": WEATHER_API_KEY, "units": "metric"}
    response = requests.get(base_url, params=params)
    if response.status_code == 200:
        data = response.json()
        print(f"DEBUG WEATHER:{data}")
        return data
    else:
        return None

def get_ai_advice(weather: dict):
    temp = weather["main"]["temp"]                # Correct path for temperature
    desc = weather["weather"][0]["description"]  # Correct path for description

    if "rain" in desc.lower():
        return "🌧️ It might rain — don't forget your umbrella!"
    elif temp > 30:
        return "☀️ It's quite hot — stay hydrated and avoid midday sun."
    elif temp < 15:
        return "🧥 It's chilly — wear something warm."
    else:
        return "😎 Great weather today — enjoy your day!"


# ---------------- CHAT MEMORY ---------------- #
chat_history = []

# ---------------- ROUTES ---------------- #
@app.get("/")
def home():
    return {"message": "AI Weather ChatBot API is running successfully!"}

@app.post("/weather")
def get_weather_info(request: CityRequest):
    weather = get_weather(request.city)
    if not weather:
        raise HTTPException(status_code=404, detail="City not found or API error.")
    forecast_item = weather["list"][0]  
    advice = get_ai_advice(forecast_item)
    return {"weather": weather, "ai_advice": advice}

@app.post("/chat")
def chat(request: ChatRequest):
    user_msg = request.message.lower()
    city = extract_city(user_msg)

    # Try to extract a city name (very basic NLP)
    if "weather" in user_msg:
        # find a city name — for now, assume last word
        words = user_msg.split()
        # city = words[-1].capitalize()
        print(f"DEBUG CITY: {city}")
        weather = get_weather(city)
        if weather:
            advice = get_ai_advice(weather)
            bot_response = (
                f"The weather in {city} is {weather['description']} with a temperature of "
                f"{weather['temperature']}°C. {advice}"
            )
        else:
            bot_response = f"Sorry, I couldn't find weather data for {city}."
    else:
        bot_response = (
            "I can tell you about the weather. Try asking like: "
            "'What's the weather in Paris?' ☁️"
        )

    chat_history.append({"user": user_msg, "bot": bot_response})
    return {"response": bot_response, "history": chat_history[-5:]}  # last 5 messages

# ---------------- SERVER ---------------- #
if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
