from django.shortcuts import render

# Create your views here.


from app.forms import *
from app.models import *
from django.urls import reverse #it will carry the data & send to the another page
from django.core.mail import send_mail #its used for sending the sending the mail
from django.contrib.auth import authenticate,login,logout #login & logout is used for user login & logout purpose
from django.contrib.auth.decorators import login_required #when user wants any changes after login, that time we must use login_required
from django.http import HttpResponse,HttpResponseRedirect #HR used for sending response #HR-redirect used for takeback the URL to the particular Page
import requests

# User registration Part
def registration (request):
    ufo=UserForm()
    pfo=ProfileForm()
    d={'ufo':ufo,'pfo':pfo}

# Checking POST Method is active or Not. & # this condition is helps to check POST method and accept the image files..

    if request.method == 'POST' and request.FILES:
        ufd=UserForm(request.POST)
        pfd=ProfileForm(request.POST,request.FILES)


# To convert Non-Modified Function Data object into Modified Function Data object (2)
    #userform module
        if ufd.is_valid() and pfd.is_valid():
            MUFDO=ufd.save(commit=False)
            pw=ufd.cleaned_data['password']
            MUFDO.set_password(pw)
            MUFDO.save()

    #profile module
            MPFDO=pfd.save(commit=False)
            MPFDO.username=MUFDO
            MPFDO.save()



# Sending the Registration Mail to User

            send_mail(
                #/Subject/
                'Registration',

                #/Message/
                'Hiii User You are Successfully Registered',

                #/From Email to Send a Mail to the User/
                'ramanikanthsasi@gmail.com',

                #/User Receipent Email/
                [MUFDO.email],

                #/fail_silently = True or False/
                #(True Means will the see the Exception otherwise False means We can't see the exception)
                fail_silently = True
                )

            return HttpResponse('Registration is Sucessfull')

        else:
            return HttpResponse('Invalid data')


      
    return render (request,'registration.html',d)


# Home Page
def home(request):
    if request.session.get('username'):
        username=request.session.get('username')
        d={'username' : username}
        return render(request,'home.html',d)
    return render (request,'home.html')


# Login
def user_login(request):
    if request.method=='POST':
        username=request.POST['un']
        password=request.POST['pw']
        AUO=authenticate(username=username,password=password)
        
        if AUO and AUO.is_active: # is_active is used to check whether the user is an active user or not
            login(request,AUO)
            request.session['username']=username # Session means it stores user's data in a file for specific time
            return HttpResponseRedirect(reverse('home'))
        else :
            return HttpResponse('Invalid Credentials')
    
    return render(request,'user_login.html')


# Logout
@login_required
def user_logout (request):
    logout(request)
    return HttpResponseRedirect(reverse('home'))


# Display the User Details
@login_required
def profile_display (request):
    un=request.session.get('username')
    uo=User.objects.get(username=un)
    po=Profile.objects.get(username=uo)
    d={'uo':uo,'po':po}
    return render(request,'profile_display.html',d)


@login_required
def change_password(request):
    if request.method =='POST':
        pw=request.POST['pw']
        username=request.session.get('username')
        UO=User.objects.get(username=username)
        UO.set_password (pw)
        UO.save()
        return HttpResponse ('password Changed Successfully!!!')
    return render (request,'change_password.html')


def reset_password(request):
    if request.method == 'POST':
        username=request.POST['un']
        password=request.POST['pw']

        LUO=user.objects.filter(username=username)
        if LUO:
            UO=LUO[0]
            UO.set_password(password)
            UO.save()
            return HttpResponse('Password is Resetted')
        else:
            return HttpResponse('Username Not Found')
    return render(request,'reset_password.html')

#-----------------------------------------------------------------------#

@login_required
def search(request):
    if request.method=='POST':
        city_name=request.POST['city']
        api_key = '30d4741c779ba94c470ca1f63045390a'
        url = f'http://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={api_key}'
        response = requests.get(url)
        weather_data = response.json()
        print(weather_data)
        temperature = weather_data['main']['temp']
        humidity = weather_data['main']['humidity']
        weather=weather_data['main']['feels_like']
        speed=weather_data['wind']['speed']
        username=request.session.get('username')
        LUO=User.objects.get(username=username)
        obj=WeatherData.objects.get_or_create(username=LUO,city=city_name, temperature=temperature, humidity=humidity,weather=weather, speed=speed)[0]
        obj.save()
        d={'obj':obj}
        return render(request,'search.html',d)
    
    return render(request,'search.html')


@login_required
def user_history(request):
    username=request.session['username']
    UO=User.objects.get(username=username)
    LWO=WeatherData.objects.filter(username=UO)

    d={'LWO':LWO}
    return render(request,'user_history.html',d)

    
def all_history(request):
    LWO=WeatherData.objects.all()
    d={'LWO':LWO}
    return render(request,'user_history.html',d)