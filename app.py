# from fastapi import FastAPI, HTTPException
# from pydantic import BaseModel
# import requests
# import os
# from dotenv import load_dotenv
# import uvicorn

# # Load environment variables
# load_dotenv()
# WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")

# app = FastAPI(
#     title="🌦️ AI Weather API",
#     version="1.0.0",
#     description="A simple AI-powered Weather API built with FastAPI."
# )

# class CityRequest(BaseModel):
#     city: str

# def get_weather(city: str):
#     base_url = "http://api.openweathermap.org/data/2.5/weather"
#     params = {"q": city, "appid": WEATHER_API_KEY, "units": "metric"}
#     response = requests.get(base_url, params=params)
#     if response.status_code == 200:
#         data = response.json()
#         return {
#             "city": data["name"],
#             "temperature": data["main"]["temp"],
#             "description": data["weather"][0]["description"],
#             "humidity": data["main"]["humidity"],
#             "wind_speed": data["wind"]["speed"]
#         }
#     else:
#         return None

# def get_ai_advice(weather: dict):
#     temp = weather["temperature"]
#     desc = weather["description"]
    
#     if "rain" in desc.lower():
#         return "🌧️ It might rain — don't forget your umbrella!"
#     elif temp > 30:
#         return "☀️ It's quite hot — stay hydrated and avoid midday sun."
#     elif temp < 15:
#         return "🧥 It's chilly — wear something warm."
#     else:
#         return "😎 Great weather today — enjoy your day!"

# @app.get("/")
# def home():
#     return {"message": "AI Weather API is running successfully!"}

# @app.post("/weather")
# def get_weather_info(request: CityRequest):
#     weather = get_weather(request.city)
#     if not weather:
#         raise HTTPException(status_code=404, detail="City not found or API error.")
#     advice = get_ai_advice(weather)
#     return {"weather": weather, "ai_advice": advice}

# if __name__ == "__main__":
#     uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)


# from fastapi import FastAPI, HTTPException
# from pydantic import BaseModel
# import requests
# import os
# from dotenv import load_dotenv
# import uvicorn

# # Load environment variables
# load_dotenv()
# WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")

# app = FastAPI(
#     title="🌦️ AI Weather API",
#     version="1.0.0",
#     description="A simple AI-powered Weather API built with FastAPI."
# )

# class CityRequest(BaseModel):
#     city: str

# def get_weather(city: str):
#     base_url = "http://api.openweathermap.org/data/2.5/weather"
#     params = {"q": city, "appid": WEATHER_API_KEY, "units": "metric"}
#     response = requests.get(base_url, params=params)
#     if response.status_code == 200:
#         data = response.json()
#         return {
#             "city": data["name"],
#             "temperature": data["main"]["temp"],
#             "description": data["weather"][0]["description"],
#             "humidity": data["main"]["humidity"],
#             "wind_speed": data["wind"]["speed"]
#         }
#     else:
#         return None

# def get_ai_advice(weather: dict):
#     temp = weather["temperature"]
#     desc = weather["description"]
    
#     if "rain" in desc.lower():
#         return "🌧️ It might rain — don't forget your umbrella!"
#     elif temp > 30:
#         return "☀️ It's quite hot — stay hydrated and avoid midday sun."
#     elif temp < 15:
#         return "🧥 It's chilly — wear something warm."
#     else:
#         return "😎 Great weather today — enjoy your day!"

# @app.get("/")
# def home():
#     return {"message": "AI Weather API is running successfully!"}

# @app.post("/weather")
# def get_weather_info(request: CityRequest):
#     weather = get_weather(request.city)
#     if not weather:
#         raise HTTPException(status_code=404, detail="City not found or API error.")
#     advice = get_ai_advice(weather)
#     return {"weather": weather, "ai_advice": advice}

# if __name__ == "__main__":
#     uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
# import requests

# API_KEY = "e8c0d00058d5a079d873193c90a74416"  # 🔹 Replace this with your actual key
# city = "London"

# url = f"http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={API_KEY}&units=metric"

# response = requests.get(url)

# if response.status_code == 200:
#     data = response.json()
#     print("City:", data["city"]["name"])
#     print("Country:", data["city"]["country"])
#     print("Forecast:")
#     for forecast in data["list"][:3]:  # print first 3 forecast entries
#         print(f"{forecast['dt_txt']}: {forecast['main']['temp']}°C, {forecast['weather'][0]['description']}")
# else:
#     print("Error:", response.status_code, response.text)

from langchain.embeddings import HuggingFaceInstructEmbeddings

embeddings = HuggingFaceInstructEmbeddings(model_name="hkunlp/instructor-large")
vector = embeddings.embed_query("Hello world")
print(vector)

