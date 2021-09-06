from controltareas.settings import SECRET
from django.http import response
from typing import Any
from django.http.request import HttpRequest
from django.http.response import HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic.edit import FormView
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth import login,logout,authenticate
from django.http import HttpResponseRedirect
from django.contrib.auth.forms import AuthenticationForm
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
import requests, jwt, json
from django.conf import settings

def decodered(request):
    data = request.COOKIES.get('validate')
    data_token = jwt.decode(data, SECRET, algorithms=["HS256"])
    return data_token

def authenticated(request):
    if request.COOKIES.get('validate'):
        data_token = decodered(request)
        if data_token['exito'] == 202:
            return True
        return False
    else:
        return False

def setcookie(tokenAPI):
    obj = redirect('dashboard')
    obj.set_cookie('validate',tokenAPI,expires=1800)
    return obj

def forgotPassword(request):
    return render(request,'login/forgot-password.html')

def lockscreen(request):
    return render(request,'login/lockscreen.html')

def recoverPassword(request):
    return render(request,'login/recover-password.html')

def validate(request):
    username = request.POST.get('username')
    password = request.POST.get('password')
    payload = {'username': username, 'password': password}
    r = requests.post('https://apitasktest.herokuapp.com/login/', data=payload)
    
    if r.ok:
        tokenAPI = r.json()
        obj = setcookie(tokenAPI['jwt'])
        return obj
    else:
        return redirect('login')
    
def Login(request):
    return render(request,'login/login.html')

# class Login(FormView):
#     template_name = "login/login.html"
#     form_class = AuthenticationForm
#     success_url = reverse_lazy('dashboard')

#     @method_decorator(csrf_protect)
#     @method_decorator(never_cache)
#     def dispatch(self,request,*args,**kwargs):
#         if request.user.is_authenticated:
#             return HttpResponseRedirect(self.get_success_url())
#         else:
#             return super(Login,self).dispatch(request,*args,*kwargs)

#     def form_valid(self,form):
#         user = authenticate(username = form.cleaned_data['username'], password = form.cleaned_data['password'])
#         token,_ = Token.objects.get_or_create(user = user)
#         if token:
#             login(self.request, form.get_user())
#             return super(Login,self).form_valid(form)
        
#     def post(self,request,*args,**kwargs):
#         return Response({'error'}, status=status.HTTP_400_BAD_REQUEST)



# class Logout(APIView):
#     def get(self,request, format = None):
#         request.user.auth_token.delete()
#         logout(request)
#         return Response(status = status.HTTP_200_OK)
    
def logout(request):
    rep = redirect("/login/")
    rep.delete_cookie('validate') # elimina el valor de la cookie de usuario establecido previamente en el navegador del usuario
    return rep


# import requests
# headers={'Content-Type':'application/json', 'Authorization':'Token d070b44498fd12728d1e1cfbc9aa5f195600d21e'}
# r = requests.get('http://localhost:8000/api/subscribers/', headers=headers)