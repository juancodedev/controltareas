import json
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
        rol = data['role']
        if int(rol) == 1:
            headers={'Content-Type':'application/json', 'Authorization': 'Bearer '+token}
            dataAPI = requests.get('http://localhost:32482/api/usuario/', headers=headers).json()
            imagen = requests.get('https://randomuser.me/api/?inc=picture&results='+str(len(dataAPI['data'])))  #api para imagenes de perfil random
            img = imagen.json()#api para imagenes de perfil random
            mylist = zip(dataAPI['data'],img['results']) #Se unen las listas de imagenes random + datos de usuario y se envian al template para mostrarlos

            context = {
                    'menu' : 'dashboard',
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
            context = {
                    'menu' : 'dashboard',
                    'email' : data['email'],
                    'name': data['unique_name'],
                    'role': int(data['role']),
                    'login' : datetime.fromtimestamp(data['nbf']),
            }
            return render(request,'home/home.html',{'datos': context})
    else:
        return redirect('login')

# def personas(request):
#     if authenticated(request):
#         cookie = decodered(request)
#         token = cookie['data']['token']
#         rol = cookie['data']['rol']
#         if rol == 1:
#             headers={'Content-Type':'application/json', 'Authorization':'Token '+token}
#             data = requests.get('https://apitasktest.herokuapp.com/API/persona/', headers=headers)
#             return HttpResponse(data, content_type='application/json')
#         else:
#             return redirect('dashboard')

#     else:
#         return redirect('login')

def tasklist(request):
    if authenticated(request):
        token = request.COOKIES.get('validate')
        data = decodered(token)
        context = {
            'menu' : 'tableTask',
            'email' : data['email'],
            'name': data['unique_name'],
            'role': int(data['role']),
            'login' : datetime.fromtimestamp(data['nbf']),
        }
        return render(request, 'task/tasklist.html',{'datos': context})
    else: 
        return redirect('login')

def teamwork(request):
    # if authenticated(request):
    #     token1 = request.COOKIES.get('validate')
    #     cookie = decodered(request)
    #     print(token1)
    #     token = cookie['data']['token']
    #     rol = cookie['rol']
    #     if rol == 1:
    #         headers={'Content-Type':'application/json', 'Authorization': 'Bearer '+token}
    #         r = requests.get('http://localhost:32482/api/usuario/', headers=headers)
    #         dataAPI= r.json()
    #         return HttpResponse(dataAPI, content_type='application/json')
    #     else:
    #         return redirect('dashboard')

    # else:
    #     return redirect('login')
    
    if authenticated(request):
        token = request.COOKIES.get('validate')
        data = decodered(token)
        rol = data['role']
        if int(rol) == 1:
            headers={'Content-Type':'application/json', 'Authorization': 'Bearer '+token}
            dataAPI = requests.get('http://localhost:32482/api/usuario/', headers=headers).json()
            roles = requests.get('http://localhost:32482/api/rol/', headers=headers).json()
            unidadinterna = requests.get('http://localhost:32482/api/unidadInterna/', headers=headers).json()
            # print(type(roles['data']))
            # print(roles['data'][0])
            # print(unidadinterna['data'])
            # # [9 if value==5 else value for value in my_list]
            
            # for item in dataAPI['data']:
            #     item['idRolUsuario'] = item['idRolUsuario'].replace('$home', item['id'])

            context = {
                'menu' : 'teamwork',
                'email' : data['email'],
                'name': data['unique_name'],
                'role': int(data['role']),
                'login' : datetime.fromtimestamp(data['nbf']),
                'teams': dataAPI['data'],
            }
            return render(request, 'teamwork/teamwork.html',{'datos': context})
        elif int(rol) == 2:
            headers={'Content-Type':'application/json', 'Authorization': 'Bearer '+token}
            dataAPI = requests.get('http://localhost:32482/api/usuario/', headers=headers).json()
            context = {
                'menu' : 'teamwork',
                'email' : data['email'],
                'name': data['unique_name'],
                'role': int(data['role']),
                'login' : datetime.fromtimestamp(data['nbf']),
                'teams': dataAPI['data'],
            }
            return render(request, 'teamwork/teamwork.html',{'datos': context})
        else:
            context = {
                    'menu' : 'dashboard',
                    'email' : data['email'],
                    'name': data['unique_name'],
                    'role': int(data['role']),
                    'login' : datetime.fromtimestamp(data['nbf']),
            }
            return render(request,'teamwork/teamwork.html',{'datos': context})
    else: 
        return redirect('login')
    
def admin(request):
    if authenticated(request):
        token = request.COOKIES.get('validate')
        data = decodered(token)
        context = {
            'menu' : 'tableTask',
            'email' : data['email'],
            'name': data['unique_name'],
            'role': int(data['role']),
            'login' : datetime.fromtimestamp(data['nbf']),
        }
        return render(request, 'task/tasklist.html',{'datos': context})
    else: 
        return redirect('login')
    
def workload(request):
    if authenticated(request):
        token = request.COOKIES.get('validate')
        data = decodered(token)
        context = {
            'menu' : 'workload',
            'email' : data['email'],
            'name': data['unique_name'],
            'role': int(data['role']),
            'login' : datetime.fromtimestamp(data['nbf']),
        }
        return render(request, 'teamwork/workload.html',{'datos': context})
    else: 
        return redirect('login')
    
def taskdetails(request):
    if authenticated(request):
        token = request.COOKIES.get('validate')
        data = decodered(token)
        context = {
            'menu' : 'taskdetails',
            'email' : data['email'],
            'name': data['unique_name'],
            'role': int(data['role']),
            'login' : datetime.fromtimestamp(data['nbf']),
        }
        return render(request, 'task/taskdetails.html',{'datos': context})
    else: 
        return redirect('login')
    
    
def tasknew(request):
    context = {
    'menu' : 'tasknew',
    'email' : 'juan@micorreo.cl',
    'name': 'juan muñoz',
    'role': 1,
    'login' : datetime.now(),
    }
    return render(request, 'task/task.html',{'datos': context})

def createnewuser(request):
    if authenticated(request):
        if request.method == 'POST':
            token = request.COOKIES.get('validate')
    #form = 
    # rut = 
    # nombre = 
    # segundonombre = 
    # apellido = 
    # segundoapellido = 
    # telefono = 
    
            payload = json.dumps({
                'RutUsuario': request.POST.get('rut'),
                'NombreUsuario': request.POST.get('name'),
                'SegundoNombre': request.POST.get('secondName'),
                'ApellidoUsuario': request.POST.get('lastName'),
                'SegundoApellido': request.POST.get('secondlastName'),
                'CorreoElectronico': request.POST.get('email'),
                'NumTelefono': request.POST.get('phoneNumber'),
                'Password': request.POST.get('password'),
                'IdRolUsuario': request.POST.get('role'),
                'IdUnidadInternaUsuario': request.POST.get('unidadInterna')
                
            })
            headers = {'Accept-Encoding': 'UTF-8', 'Content-Type': 'application/json', 'Accept': '*/*', 'Authorization': 'Bearer '+token}

    # password = request.POST.get('password')
    # payload = json.dumps({'email': email, 'password': password})
            r = requests.post('http://localhost:32482/api/usuario/add', headers=headers, data=payload)
            if r.ok:
                print('Usuario creado correctamente')
            else:
                print('Error')
    else: 
        return redirect('login')
    
    
#     {


# }
    
def newuser(request):
    context = {
    'menu' : 'newuser',
    'email' : 'juan@micorreo.cl',
    'name': 'juan muñoz',
    'role': 1,
    'login' : datetime.now(),
    }
    return render(request, 'users/newuser.html',{'datos': context})

def listusers(request):
    context = {
    'menu' : 'listusers',
    'email' : 'juan@micorreo.cl',
    'name': 'juan muñoz',
    'role': 1,
    'login' : datetime.now(),
    }
    return render(request, 'users/userlist.html',{'datos': context})


def newunits(request):
    context = {
    'menu' : 'newunits',
    'email' : 'juan@micorreo.cl',
    'name': 'juan muñoz',
    'role': 1,
    'login' : datetime.now(),
    }
    return render(request, 'units/units.html',{'datos': context})

def listunits(request):
    context = {
    'menu' : 'listunits',
    'email' : 'juan@micorreo.cl',
    'name': 'juan muñoz',
    'role': 1,
    'login' : datetime.now(),
    }
    return render(request, 'units/unitslist.html',{'datos': context})




def newrole(request):
    context = {
    'menu' : 'newrole',
    'email' : 'juan@micorreo.cl',
    'name': 'juan muñoz',
    'role': 1,
    'login' : datetime.now(),
    }
    return render(request, 'role/role.html',{'datos': context})


def workflowlist(request):
    context = {
    'menu' : 'workflowlist',
    'email' : 'juan@micorreo.cl',
    'name': 'juan muñoz',
    'role': 3,
    'login' : datetime.now(),
    }
    return render(request, 'workflow/workflowlist.html',{'datos': context})

def workflownew(request):
    context = {
    'menu' : 'workflownew',
    'email' : 'juan@micorreo.cl',
    'name': 'juan muñoz',
    'role': 1,
    'login' : datetime.now(),
    }
    return render(request, 'workflow/workflownew.html',{'datos': context})

def workflowview(request):
    context = {
    'menu' : 'workflowview',
    'email' : 'juan@micorreo.cl',
    'name': 'juan muñoz',
    'role': 1,
    'login' : datetime.now(),
    }
    return render(request, 'workflow/workflowview.html',{'datos': context})

def workflowhistory(request):
    context = {
    'menu' : 'workflowhistory',
    'email' : 'juan@micorreo.cl',
    'name': 'juan muñoz',
    'role': 3,
    'login' : datetime.now(),
    }
    return render(request, 'workflow/workflowhistory.html',{'datos': context})


def listrole(request):
    context = {
    'menu' : 'listrole',
    'email' : 'juan@micorreo.cl',
    'name': 'juan muñoz',
    'role': 1,
    'login' : datetime.now(),
    }
    return render(request, 'role/rolelist.html',{'datos': context})

#Metodos para perfil funcionario

def taskfuncionario(request):
    context = {
    'menu' : 'taskfuncionario',
    'email' : 'juan@micorreo.cl',
    'name': 'juan muñoz',
    'role': 2,
    'login' : datetime.now(),
    }
    return render(request, 'task/tasklist.html',{'datos': context})


def messagelist(request):
    context = {
    'menu' : 'messagelist',
    'email' : 'juan@micorreo.cl',
    'name': 'juan muñoz',
    'role': 2,
    'login' : datetime.now(),
    }
    return render(request, 'messages/messagelist.html',{'datos': context})

def messagereaded(request):
    context = {
    'menu' : 'messagereaded',
    'email' : 'juan@micorreo.cl',
    'name': 'juan muñoz',
    'role': 2,
    'login' : datetime.now(),
    }
    return render(request, 'messages/messagereaded.html',{'datos': context})

def messageresponded(request):
    context = {
    'menu' : 'messageresponded',
    'email' : 'juan@micorreo.cl',
    'name': 'juan muñoz',
    'role': 2,
    'login' : datetime.now(),
    }
    return render(request, 'messages/messageresponded.html',{'datos': context})
