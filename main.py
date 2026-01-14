import datetime
import sys
import time
import pyautogui
import pyttsx3
import speech_recognition as sr
import webbrowser
import os
import json
import pickle
from tensorflow import keras
from tensorflow.keras.models import load_model #type: ignore
from tensorflow.keras.preprocessing.sequence import pad_sequences # type: ignore
from tensorflow.keras.models import Sequential  # type: ignore
from tensorflow.keras.layers import Dense, Embedding, GlobalAveragePooling1D  # type: ignore
from tensorflow.keras.preprocessing.text import Tokenizer  # type: ignore
import random
import numpy as np
import psutil

with open("intents.json") as file:
    data = json.load(file)

model = load_model("chat_model.h5")

with open("tokenizer.pkl", "rb") as f:
    tokenizer = pickle.load(f)

with open("label_encoder.pkl", "rb") as encoder_file:
   label_encoder = pickle.load(encoder_file)

def initialize_engine():
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[7].id)
    rate = engine.getProperty('rate')
    engine.setProperty('rate', rate-50)
    volume = engine.getProperty('volume')
    engine.setProperty('volume', volume+0.25)
    return engine

def speak(text):
    engine = initialize_engine()
    engine.say(text)
    engine.runAndWait()

def command():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source, duration=1.0)
        print("Listening.......", end="", flush=True)
        r.pause_threshold=1.0
        r.phrase_threshold=0.3
        r.sample_rate = 48000
        r.dynamic_energy_threshold=True
        r.operation_timeout=5
        r.non_speaking_duration=0.5
        r.dynamic_energy_adjustment=2
        r.energy_threshold=4000
        r.phrase_time_limit = 10
        audio = r.listen(source, timeout=10)
    try:
        print("\r" ,end="", flush=True)
        print("Recognizing......", end="", flush=True)
        query = r.recognize_google(audio, language='en-in')
        print("\r" ,end="", flush=True)
        print(f"User said : {query}\n")
    except Exception as e:
        print("Say that again please")
        return "None"
    return query

def cal_day():
    day = datetime.datetime.today().weekday() + 1
    day_dict={
        1:"Monday",
        2:"Tuesday",
        3:"Wednesday",
        4:"Thursday",
        5:"Friday",
        6:"Saturday",
        7:"Sunday"
    }
    if day in day_dict.keys():
        day_of_week = day_dict[day]
        print(day_of_week)
    return day_of_week

def wishMe():
    hour = int(datetime.datetime.now().hour)
    t = time.strftime("%I:%M:%p")
    day = cal_day()

    if(hour >= 0) and (hour <= 12) and ('AM' in t):
        speak(f"Good Morning JD, it's {day} and the time is {t}")
    elif(hour >= 12) and (hour <= 16) and ('PM' in t):
        speak(f"Good Afternoon JD, it's {day} and the time is {t}")
    else:
        speak(f"Good Evening JD, it's {day} and the time is {t}")

def social_media(command):
    if 'youtube' in command:
        speak("opening youtube")
        webbrowser.open("https://www.youtube.com/")
    elif 'instagram' in command:
        speak("opening instagram")
        webbrowser.open("https://instagram.com/")
    elif 'discord' in command:
        speak("opening discord")
        webbrowser.open("https://discord.com/")
    elif 'tiktok' in command:
        speak("opening tiktok")
        webbrowser.open("https://www.tiktok.com/")
    else:
        speak("no result found")

def schedule():
    day = cal_day().lower()
    speak("JD today's schedule is ")
    week = {
        "monday": "Boss you have wrestling practice today as well as hill sprints",
        "tuesday": "Boss you have jiu jitsu practice today as well as long distance running",
        "wednesday": "Boss you have strength training today so lift your hardest",
        "thursday": "Today is a rest day but that doesn't mean sit on the couch all day do some light cardio",
        "friday": "Boss you have muay thai practice today and you are sparring with shashank so be careful",
        "saturday": "Boss you have Boxing practice today as well as your performance test",
        "sunday": "Boss you have strength training today so lift your hardest"
    }
    if day in week.keys():
        speak(week[day])

def openApp(command):
    if "calculator" in command:
        speak("opening calculator")
        os.system('open /System/Applications/Calculator.app')
    elif "notepad" in command:
        speak("opening text editor")
        os.system('open /System/Applications/Notes.app')
    elif "calendar" in command:
        speak("opening calendar app")
        os.system('open /System/Applications/Calendar.app')
    elif "games" in command:
        speak("opening games")
        os.system('open /System/Applications/Games.app')

def closeApp(command):
    if "calculator" in command:
        speak("closing calculator")
        os.system('osascript -e \'quit app "Calculator"\'')
    elif "notepad" in command:
        speak("closing notepad")
        os.system('osascript -e \'quit app "Notes"\'')
    elif "calendar" in command:
        speak("closing calendar")
        os.system('osascript -e \'quit app "Calendar"\'')
    elif "games" in command:
        speak("closing games")
        os.system('osascript -e \'quit app "Games"\'')

def browsing(query):
    if 'google' in query.lower():
        speak("JD, what should I search for?")
        c = command().lower()
        
        search_query = c.replace(' ', '+')
        google_url = f"https://www.google.com/search?q={search_query}"
        
        print(f"Opening: {google_url}")
        webbrowser.open(google_url)
        speak(f"Searching Google for {c}")

def conditions():
    usage = str(psutil.cpu_percent())
    speak(f"CPU is at {usage} percentage")
    battery = psutil.sensors_battery()
    percentage = battery.percent
    speak(f"JD the computer is at {percentage} percentage battery")


if __name__ == "__main__":
    wishMe()
    while True:
        query = command().lower()
        if ('youtube' in query) or ('instagram' in query) or ('discord' in query) or ('tiktok' in query):
            social_media(query)
        elif ("schedule" in query):
            schedule()
        elif ("volume up" in query) or ("increase volume" in query):
            pyautogui.press("volumeup")
            speak("Increased volume")
        elif ("volume down" in query) or ("decrease volume" in query):
            pyautogui.press("volumedown")
            speak("Decreased volume")
        elif ("volume mute" in query) or ("mute the sound" in query):
            pyautogui.press("volumemute")
            speak("Muted volume")
        elif ("open calculator" in query) or ("open calendar" in query) or ("open games" in query) or ("open notepad" in query):
            openApp(query)
        elif ("close calculator" in query) or ("close calendar" in query) or ("close games" in query) or ("close notepad" in query):
            closeApp(query)
        elif ("what" in query) or ("who" in query) or ("how" in query) or ("hi" in query) or ("thanks" in query) or ("hello" in query):
            padded_sequences = pad_sequences(tokenizer.texts_to_sequences([query]), maxlen=20, truncating='post')
            result = model.predict(padded_sequences)
            tag = label_encoder.inverse_transform([np.argmax(result)])

            for i in data['intents']:
                if i['tag'] == tag: 
                    response = np.random.choice(i["responses"])
                    print(response)
                    speak(response)
        elif("open google" in query):
            browsing(query)
        elif("system condition" in query) or ("condition of the system" in query):
            speak("checking the system's conditions")
            conditions()
        elif "exit" in query:
            speak("Goodbye JD")
            sys.exit()
