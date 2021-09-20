from django.http.request import HttpHeaders
from django.shortcuts import render, redirect
from django.http import HttpResponse
from login.views import authenticated, decodered
import requests
from datetime import datetime

def dashboard(request):
    if authenticated(request):
        token = request.COOKIES.get('validate')
        data = decodered(token)
        headers={'Content-Type':'application/json', 'Authorization': 'Bearer '+token}
        r = requests.get('http://localhost:32482/api/usuario/', headers=headers)
        dataAPI= r.json()
        imagen = requests.get('https://randomuser.me/api/?inc=picture&results='+str(len(dataAPI['data'])))  #api para imagenes de perfil random
        img = imagen.json()#api para imagenes de perfil random
        mylist = zip(dataAPI['data'],img['results']) #Se unen las listas de imagenes random + datos de usuario y se envian al template para mostrarlos

        context = {
                'email' : data['email'],
                'name': data['unique_name'],
                'role': int(data['role']),
                'login' : datetime.fromtimestamp(data['nbf']),
                # 'usuarios' : dataAPI['data'],
                # 'img' : img['results'],
                'usuarios': mylist, 
        }
        return render(request,'home/home.html',{'datos': context})
    else:
        return redirect('login')

def personas(request):
    if authenticated(request):
        cookie = decodered(request)
        token = cookie['data']['token']
        rol = cookie['data']['rol']
        if rol == 1:
            headers={'Content-Type':'application/json', 'Authorization':'Token '+token}
            data = requests.get('https://apitasktest.herokuapp.com/API/persona/', headers=headers)
            return HttpResponse(data, content_type='application/json')
        else:
            return redirect('dashboard')

    else:
        return redirect('login')

def tableTask(request):
    if authenticated(request):
        token = request.COOKIES.get('validate')
        data = decodered(token)
        context = {
            'email' : data['email'],
            'name': data['unique_name'],
            'role': int(data['role']),
            'login' : datetime.fromtimestamp(data['nbf']),
        }
        return render(request, 'pages/tables/simple.html',{'datos': context})
    else: 
        return redirect('login')
