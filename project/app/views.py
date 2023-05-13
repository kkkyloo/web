from django.shortcuts import render
import urllib.request
import json

# Create your views here.
def home(request):
    try:
        if request.method == 'POST':
            
            city = request.POST['city']
            source = urllib.request.urlopen('http://api.openweathermap.org/data/2.5/weather?q='+city+'&units=metric&appid=a15417c7ebe0bcce38f2aabdd96f2549').read()
            
            list_of_data =json.loads(source)

            print(list_of_data)

            data ={
                'country_code':str(list_of_data['sys']['country']),
                'cor':str(list_of_data["coord"]["lon"])+" "+str(list_of_data["coord"]["lat"]) +" °",
                'temp':str(list_of_data["main"]['temp'])+" °C",
                'pressure':str(list_of_data['main']["pressure"]) +" мм рт. ст.",
                'humidity':str(list_of_data['main']['humidity'])+"%",
                'main':str(list_of_data["weather"][0]['main']),   
                'description':str(list_of_data["weather"][0]['description']), 
                'icon':list_of_data["weather"][0]['icon'],
                'speed': str(list_of_data['wind']['speed'])+" м/с",
                'city':city
            }
        else:
            data ={}

        return render(request,'weather.html',data)
    except:
        data ={
                'country_code': str("Неправильно введен город."),
                'cor':str(" "),
                'temp':str(" "),
                'pressure':str(" "),
                'humidity':str(" "),
                'main':str(" "),
                'description':str(" "),
                'icon':str(" "),
                'speed': str(" "),
                'city':city
            }
        return render(request,'weather.html',data)