from django.http.request import HttpHeaders
from django.shortcuts import render, redirect
from django.http import HttpResponse
from login.views import authenticated, decodered
import requests

def dashboard(request):
    if authenticated(request):
        return render(request,'home/dashboard.html')#,{'data': data['data']})
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
