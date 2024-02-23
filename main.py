import json
import requests
import speech_recognition as sr
from datetime import datetime
import webbrowser
import time
from gtts import gTTS
import random
import os
import pygame



def get_recipe(food):
    app_id = "cbeeced7"
    app_key = "fd27e5062ddf261cbf678d169d84a9dd"
    url = f"https://api.edamam.com/search?q={food}&app_id={app_id}&app_key={app_key}"
    response = requests.get(url)
    data = response.json()
    if "hits" in data and data["hits"]:
        recipe = data['hits'][0]['recipe']
        recipe_name = recipe['label']
        recipe_url = recipe['url']
        return recipe_name, recipe_url
    else:
        return None, None

def get_api_key(api_name):
    with open("config.json") as f:
        config = json.load(f)
        return config[api_name]

def record(ask=False):
    r = sr.Recognizer()
    with sr.Microphone() as source:
        if ask:
            speak(ask)
        print("Mikrofon dinleniyor..")
        audi = r.listen(source)
        voice = ''
        try:
            voice = r.recognize_google(audi, language='tr-TR')
        except sr.UnknownValueError:
            speak('anlayamadım.')
        except sr.RequestError:
            speak('sistem çalışmıyor.')
        return voice
def get_weather(city):
    api_key = get_api_key("openweathermap_api_key")
    base_url = "http://api.openweathermap.org/data/2.5/weather?"
    complete_url = f"{base_url}q={city}&appid={api_key}&units=metric"
    response = requests.get(complete_url)
    data = response.json()
    if data["cod"] != "404":
        main = data["main"]
        temperature = main["temp"]
        humidity = main["humidity"]
        weather = data["weather"]
        weather_description = weather[0]["description"]
        return f"{city} şehrinde hava sıcaklığı {temperature} derece, nem oranı %{humidity} ve {weather_description}"
    else:
        return "Şehir bulunamadı"


def speak(string):
    tts = gTTS(string, lang='tr')
    rand = random.randint(1, 10000)
    file_path = 'audio-' + str(rand) + '.mp3'
    tts.save(file_path)

    pygame.mixer.init()
    pygame.mixer.music.load(file_path)
    pygame.mixer.music.play()

    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(1)

    pygame.mixer.music.stop()
    pygame.mixer.quit()
    os.remove(file_path)

def response(voice):
    if 'nasılsın' in voice:
        speak('Elhamdulillah iyim sen nasılsın Enes.')

    elif 'saat kaç' in voice:
        speak(datetime.now().strftime('%H:%M:%S'))

    elif 'bugünün tarihi' in voice:
        speak(datetime.now().strftime('%d:%B:%Y:%A'))

    elif 'hava durumu' in voice:
        speak("Hangi şehrin hava durumunu öğrenmek istiyorsun?")
        city = record()
        weather_info = get_weather(city)
        speak(weather_info)

    elif 'arama yapabilir misin' in voice:
        search = record('ne aramak istiyorsun')
        url = 'https://www.google.com/search?q={}'.format(search)
        webbrowser.open(url)
        speak(search + ' için bulduklarım ')

    elif 'seyahat bilgilerine git' in voice:
        speak("Hangi şehirler arasındaki seyahat bilgilerini öğrenmek istiyorsun?")
        speak("Başlangıç noktasını söyler misin?")
        origin = record()
        speak("Varış noktasını söyler misin?")
        destination = record()
        travel_info = get_travel_info(origin, destination)
        speak(travel_info)

    elif 'yemek tarifi' in voice:
        speak("Hangi yemek tarifini aramak istiyorsunuz?")
        food = record()
        recipe_name, recipe_url = get_recipe(food)
        if recipe_name and recipe_url:
            speak(f"Bir tarif buldum: {recipe_name}. Tarifin linki'i görmek istiyor musunuz?")
            confirm = record("Tarifin linki'i görmek istiyor musunuz?")
            if "evet" in confirm:
                speak(f"Tarifin linki'i şurada: {recipe_url}")
                webbrowser.open(recipe_url)
            else:
                speak("Anladım.")
        else:
            speak("Üzgünüm, tarif bulunamadı.")

    elif 'hisse senedi fiyatı' in voice:
        speak("Hangi hisse senedi fiyatını öğrenmek istiyorsun?")
        symbol = record()
        stock_price = get_stock_price(symbol)
        speak(stock_price)

    elif 'tamamdır' in voice:
        speak('görüşürüz')
        exit()
    else:
        speak("Anlamadım, bir şey yapmam gerekmiyorsa sormaya devam edebilirsiniz.")

speak('Merhaba ben yapay zeka asistanınız. nasıl yardımcı olabilirim ?')
time.sleep(1)
while True:
    speak2 = False
    voice = record()
    print(voice)
    if voice:
        response(voice)

