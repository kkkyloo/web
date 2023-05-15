from django.shortcuts import render
import requests
from .config import open_weather_token

def home(request):
    try:
        r = requests.get(f"http://api.openweathermap.org/data/2.5/weather?q=Ростов-на-Дону&appid={open_weather_token}&units=metric&lang=ru")
        data = r.json()
 
        city = data["name"]
        cur_weather = data["main"]["temp"]
        wind = data["wind"]["speed"]

        
        data ={
            'city':str(city),
            'temp':str(cur_weather)+" °C",
            'speed': str(wind)+" м/с"
        }


        return render(request, 'weather.html',data)
    
    except:
        data ={
                'temp':str(" "),
                'city':str(" "),
                'speed':str(" "),
            }
        return render(request, 'weather.html',data)