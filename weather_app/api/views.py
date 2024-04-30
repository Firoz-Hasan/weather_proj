from django.shortcuts import render
import urllib.request
import json
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.hashers import make_password
# Create your views here.


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
       
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            request.session['username'] = username 
            print("Username stored in session:", request.session['username'])  # Debugging
            return redirect('index')
        else:
            return render(request, 'login.html', {'error': 'Invalid username or password'})
    else:
        return render(request, 'login.html')
    
def register_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        if password == confirm_password:
            # Check if username already exists
            if User.objects.filter(username=username).exists():
                messages.error(request, 'Username already exists')
                return redirect('register')
            else:
                # Create new user with hashed password
                hashed_password = make_password(password)
                user = User.objects.create_user(username=username, password=password)
                login(request, user)
                request.session['username'] = username
                return redirect('login')
        else:
            messages.error(request, 'Passwords do not match')
            return redirect('register')
    else:
        return render(request, 'register.html')
    
def index(request):
    username = request.session.get('username')
    print ('-------------------------------',username)
    if request.method == 'POST':
        city = request.POST.get('city')
        data = get_weather_data(city)
    elif username:
        city = 'Cambridge'
        data = get_weather_data(city)
    else:
        city = None
        data = {
            "country": None,
            "weather_description": None,
            "weather_temperature": None,
            "weather_pressure": None,
            "weather_humidity": None,
            "weather_icon": None,
        }
    return render(request, 'index.html', {"city": city, "data": data, "username": username})

def get_weather_data(city):
    api_url = urllib.request.urlopen('http://api.openweathermap.org/data/2.5/weather?q=' + city + '&appid=a3152a12a06fdbcd108c77739a948965').read()
    api_url2 = json.loads(api_url)
    weather_data = {
        "country": city,
        "weather_description": api_url2['weather'][0]['description'],
        "weather_temperature": api_url2['main']['temp'],
        "weather_pressure": api_url2['main']['pressure'],
        "weather_humidity": api_url2['main']['humidity'],
        "weather_icon": api_url2['weather'][0]['icon'],
    }
    return weather_data
    
    