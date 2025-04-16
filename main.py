from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama.llms import OllamaLLM
import ollama
import pyttsx3
import speech_recognition as sr
import os, webbrowser
import requests
from dotenv import load_dotenv

engine = pyttsx3.init()
engine.setProperty('rate', 150)    
engine.setProperty('volume', 0.9)  

OPEN_WEATHER_API_KEY = os.getenv("OPEN_WEATHER_API_KEY")

def get_weather(city="Folsom"):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={OPEN_WEATHER_API_KEY}&units=imperial"
    try:
        response = requests.get(url)
        data = response.json()
        if data["cod"] != "404":
            main = data["main"]
            weather_desc = data["weather"][0]["description"]
            temperature = main["temp"]
            temp_max = main["temp_max"]
            return f"The weather in {city} is {weather_desc} with a temperature of {temperature}°F and a max of {temp_max}°F."
    except Exception as e:
        return "Sorry, I couldn't fetch the weather data."

def handle_command(text):
    text = text.lower()

    if "open youtube" in text:
        webbrowser.open("https://www.youtube.com")
        return "Opening YouTube..."
    elif "open google" in text:
        webbrowser.open("https://www.google.com")
        return "Opening Google..."
    elif "open gmail" in text:
        webbrowser.open("https://mail.google.com")
        return "Opening Gmail..."
    elif "open google classroom" in text:
        webbrowser.open("https://classroom.google.com")
        return "Opening Google Classroom..."
    elif "weather" in text or "what's the weather" in text:
        return get_weather(city="Folsom")
    elif "stop" in text:
        return "Stopping the assistant."
    
    return None

def listen_for_jarvis():
    r = sr.Recognizer()
    r.energy_threshold = 4000
    r.dynamic_energy_threshold = True
    with sr.Microphone() as source:
        print("Listening for 'Jarvis'...")
        audio = r.listen(source)

    try:
        text = r.recognize_google(audio, language="en-US")
        return text
    
    except sr.UnknownValueError:
        print("Could not understand the audio")
        engine.say("Sorry, I did not understand that. Could you repeat?")
        engine.runAndWait()
        return ""
    

text = ""
while True:
    text = listen_for_jarvis()
    
    if "jarvis" in text.lower():
        engine.say("Jarvis is activated, how can I help you?")
        engine.runAndWait()
        break  

while text != "stop":
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening for command...")
        audio = r.listen(source, timeout=5)
        text = r.recognize_google(audio)

    try:
        command_response = handle_command(text)
        if command_response:
            engine.say(command_response)
            engine.runAndWait()
            
            if text.lower() == "stop":
                break 
            continue  

        template = """
        You are a helpful assistant. You are an interactive chatbot that can answer questions and provide information. 
        Your job is to have a conversation with the human user and provide helpful and informative responses.
        Have a structured conversation, do not respond with long answers unless necessary.
        The user asked: {question}
        """

        prompt = ChatPromptTemplate.from_template(template)

        response = ollama.chat(
            model="llama3.2",
            messages=[{
                "role": "user",
                "content": template.format(question=text)
            }]
        )

        x = response["message"]["content"]
        engine.say(x)
        engine.runAndWait()

    except sr.exceptions.UnknownValueError:
        print("Could not understand the audio")
        engine.say("Sorry, I did not understand that. Could you repeat?")
        engine.runAndWait()
    