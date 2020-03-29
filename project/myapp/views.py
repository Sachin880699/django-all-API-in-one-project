from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib import auth

import json
# urllib.request to make a request to api
import urllib.request


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

    data = request.POST.get('name')
    import wikipedia
    data = wikipedia.summary(data,sentences=2)

    return render(request,'wikipedia.html',{'data':data})

def weather(request):
    if request.method == 'POST':
        city = request.POST['city']
        ''' api key might be expired use your own api_key 
            place api_key in place of appid ="your_api_key_here "  '''

        # source contain JSON data from API

        source = urllib.request.urlopen(
            'http://api.openweathermap.org/data/2.5/weather?q ='
            + city + '&appid = 00d1693ce529e18035487523049e4d8f').read()

        # converting JSON data to a dictionary
        list_of_data = json.loads(source)

        # data for variable list_of_data
        data = {
            "country_code": str(list_of_data['sys']['country']),
            "coordinate": str(list_of_data['coord']['lon']) + ' '
                          + str(list_of_data['coord']['lat']),
            "temp": str(list_of_data['main']['temp']) + 'k',
            "pressure": str(list_of_data['main']['pressure']),
            "humidity": str(list_of_data['main']['humidity']),
        }
        print(data)
    else:
        data = {}
    return render(request,'weather.html',{'data':data})