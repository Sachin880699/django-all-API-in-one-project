from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib import auth
import wikipedia
import requests, json

def home(request):
    return render(request,'home.html')



def signup(request):
    if request.method == 'POST':
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.get(username=request.POST['username'])
                return render(request, 'signup.html', {'error':'Username is already taken'})
            except User.DoesNotExist:
                user = User.objects.create_user(request.POST['username'], password=request.POST['password1'],email=request.POST['email'])
                auth.login(request, user)
                return redirect('home')

        else:
            return render(request, 'signup.html', {'error':'Password doesn\'t matched'})

    else:
        return render(request, 'signup.html')



def login(request):
    if request.method == 'POST':
        user = auth.authenticate(username=request.POST['username'], password=request.POST['password'])
        if user is not None:
            auth.login(request, user)
            return redirect('home')
        else:
            return render(request, 'login.html', {'error':'username or password is incorrect!'})

    else:
        return render(request, 'login.html')


def logout(request):
    if request.method == 'POST':
        auth.logout(request)
        return redirect('home')


def wikipedia(request):
    #data = wikipedia.summary("Key (cryptography)")



    return render(request,'wikipedia.html')

def weather(request):
    data = request.POST.get('input',"")
    print(data)

    # Python program to find current
    # weather details of any city
    # using openweathermap api

    # import required modules


    # Enter your API key here
    api_key = "00d1693ce529e18035487523049e4d8f"

    # base_url variable to store url
    base_url = "http://api.openweathermap.org/data/2.5/weather?"

    # Give city name
    city_name = data

    # complete_url variable to store
    # complete url address
    complete_url = base_url + "appid=" + api_key + "&q=" + city_name

    # get method of requests module
    # return response object
    response = requests.get(complete_url)

    # json method of response object
    # convert json format data into
    # python format data
    x = response.json()

    # Now x contains list of nested dictionaries
    # Check the value of "cod" key is equal to
    # "404", means city is found otherwise,
    # city is not found
    if x["cod"] != "404":
        # store the value of "main"
        # key in variable y
        y = x["main"]

        # store the value corresponding
        # to the "temp" key of y
        current_temperature = y["temp"]

        # store the value corresponding
        # to the "pressure" key of y
        current_pressure = y["pressure"]

        # store the value corresponding
        # to the "humidity" key of y
        current_humidiy = y["humidity"]

        # store the value of "weather"
        # key in variable z
        z = x["weather"]

        # store the value corresponding
        # to the "description" key at
        # the 0th index of z
        weather_description = z[0]["description"]

        # print following values
        '''print(" Temperature (in kelvin unit) = " +
              str(current_temperature) +
              "\n atmospheric pressure (in hPa unit) = " +
              str(current_pressure) +
              "\n humidity (in percentage) = " +
              str(current_humidiy) +
              "\n description = " +
              str(weather_description))'''

        data = {
            'current_temperature': current_temperature,
            'current_pressure': current_pressure,
            "current_humidiy":current_humidiy,
            "weather_description":weather_description
        }

    else:
        error = "Sorry city not match"

    return render(request,'weather.html',{"data":data})