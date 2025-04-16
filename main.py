from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import AIMessage, HumanMessage
from langchain_ollama.llms import OllamaLLM
import ollama
import pyttsx3
import speech_recognition as sr
import os, webbrowser
import requests
import time
from dotenv import load_dotenv

engine = pyttsx3.init()
engine.setProperty('rate', 200)    
engine.setProperty('volume', 0.9)  

OPEN_WEATHER_API_KEY = os.getenv("OPEN_WEATHER_API_KEY")

conversation_history = []

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
    elif "stop" in text or "pause" in text:
        return "Going back to standby mode. Say 'Jarvis' to activate me again."
    elif "clear memory" in text or "forget our conversation" in text:
        global conversation_history
        conversation_history = []
        return "Memory cleared. I've forgotten our previous conversation."
    elif "exit program" in text or "shutdown" in text:
        print("Shutting down Jarvis assistant...")
        return "Shutting down Jarvis assistant. Goodbye!"
    
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
        print(f"Heard: {text}")
        return text
    
    except sr.UnknownValueError:
        print("Could not understand the audio")
        return ""

def listen_for_command(timeout=30):
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print(f"Listening for command (timeout in {timeout} seconds)...")
        try:
            audio = r.listen(source, timeout=5, phrase_time_limit=timeout)
            text = r.recognize_google(audio)
            print(f"User said: {text}")
            return text
        except sr.WaitTimeoutError:
            print("No speech detected within timeout period")
            return "TIMEOUT"
        except sr.UnknownValueError:
            print("Could not understand the audio")
            return "UNKNOWN"
        except sr.RequestError:
            print("Could not request results from Google Speech Recognition service")
            return "ERROR"

def main():
    global conversation_history
    
    while True:  
        print("Waiting for activation word...")
        while True:
            text = listen_for_jarvis()
            
            if "jarvis" in text.lower():
                engine.say("Jarvis is activated, how can I help you?")
                engine.runAndWait()
                break
        
        last_activity_time = time.time()
        
        while True:
            if time.time() - last_activity_time > 30:
                print("Inactive for 30 seconds, returning to standby mode")
                engine.say("No activity detected. Going back to standby mode.")
                engine.runAndWait()
                break

            text = listen_for_command(timeout=10)
            
            if text not in ["TIMEOUT", "UNKNOWN", "ERROR"]:
                last_activity_time = time.time()
            
            if text == "TIMEOUT":
                print("Timeout reached, returning to standby mode")
                engine.say("No activity detected. Going back to standby mode.")
                engine.runAndWait()
                break
            elif text == "UNKNOWN" or text == "ERROR":
                engine.say("Sorry, I did not understand that. Could you repeat?")
                engine.runAndWait()
                continue

            try:
                command_response = handle_command(text)
                if command_response:
                    engine.say(command_response)
                    engine.runAndWait()
                    
                    if "exit program" in text.lower() or "shutdown" in text.lower():
                        return  
                    elif "stop" in text.lower() or "pause" in text.lower():
                        break 
                    continue

                conversation_history.append(HumanMessage(content=text))

                template = """
                You are a helpful assistant named Jarvis. You are an interactive chatbot that can answer questions and provide information.
                Your job is to have a conversation with the human user and provide helpful and informative responses.
                Have a structured conversation, do not respond with long answers unless necessary.

                Do NOT be annoying or repetitive. Do NOT be extra. Only carry out tasks and answer questions.
                
                Conversation history:
                {history}
                
                The user asked: {question}
                """

                history_text = ""
                for msg in conversation_history:
                    if isinstance(msg, HumanMessage):
                        history_text += f"Human: {msg.content}\n"
                    else:
                        history_text += f"Jarvis: {msg.content}\n"
                
                prompt = template.format(history=history_text, question=text)

                response = ollama.chat(
                    model="llama3.2",
                    messages=[{
                        "role": "user",
                        "content": prompt
                    }]
                )

                x = response["message"]["content"]
                
                conversation_history.append(AIMessage(content=x))
                
                if len(conversation_history) > 10:  
                    conversation_history = conversation_history[-10:]
                    
                engine.say(x)
                engine.runAndWait()
                
                last_activity_time = time.time()

            except Exception as e:
                print(f"Error: {e}")
                engine.say("I encountered an error. Please try again.")
                engine.runAndWait()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nProgram terminated by user.")
