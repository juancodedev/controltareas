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

#Lista de detalle de las tareas creadas
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
    
#Creacion de tareas 
def tasknew(request):
    if authenticated(request):
        token = request.COOKIES.get('validate')
        data = decodered(token)
        headers = {'Accept-Encoding': 'UTF-8', 'Content-Type': 'application/json', 'Accept': '*/*', 'Authorization': 'Bearer '+token}
        payload = json.dumps({
            'rutUsuario': request.POST.get('rut'),
            'nombreUsuario': request.POST.get('name'),
            'segundoNombre': request.POST.get('secondName'),
            'apellidoUsuario': request.POST.get('lastName'),
            'segundoApellido': request.POST.get('secondlastName'),
            'correoElectronico': request.POST.get('email'),
            'numTelefono': int(request.POST.get('phoneNumber')),
            'password': request.POST.get('password'),
            'idRolUsuario': int(request.POST.get('role')),
            'idUnidadInternaUsuario': int(request.POST.get('unidadInterna'))

        })
        r = requests.post('http://localhost:32482/api/usuario/add', headers=headers, data=payload)
        if r.ok:
            print('Usuario creado correctamente')
        else:
            print('Error')
        context = {
            'menu' : 'tasknew',
            'email' : data['email'],
            'name': data['unique_name'],
            'role': int(data['role']),
            'login' : datetime.fromtimestamp(data['nbf']),
        }
        return render(request, 'task/task.html',{'datos': context})
    else: 
        return redirect('login')

    

#Creacion de nuevos usuarios
def createnewuser(request):
    if authenticated(request):
        token = request.COOKIES.get('validate')
        data = decodered(token)
        headers = {'Accept-Encoding': 'UTF-8', 'Content-Type': 'application/json', 'Accept': '*/*', 'Authorization': 'Bearer '+token}
        payload = json.dumps({
            'rutUsuario': request.POST.get('rut'),
            'nombreUsuario': request.POST.get('name'),
            'segundoNombre': request.POST.get('secondName'),
            'apellidoUsuario': request.POST.get('lastName'),
            'segundoApellido': request.POST.get('secondlastName'),
            'correoElectronico': request.POST.get('email'),
            'numTelefono': int(request.POST.get('phoneNumber')),
            'password': request.POST.get('password'),
            'idRolUsuario': int(request.POST.get('role')),
            'idUnidadInternaUsuario': int(request.POST.get('unidadInterna'))
            
        })
        r = requests.post('http://localhost:32482/api/usuario/add', headers=headers, data=payload)
        if r.ok:
            print('Usuario creado correctamente')
        else:
            print('Error')
        context = {
        'menu' : 'newuser',
        'email' : data['email'],
        'name': data['unique_name'],
        'role': int(data['role']),
        'login' : datetime.fromtimestamp(data['nbf']),
        }
        return render(request, 'users/newuser.html',{'datos': context})

    else: 
        return redirect('login')
    

#Renderizado de template de creacion de usuarios 
def newuser(request):
    if authenticated(request):
        token = request.COOKIES.get('validate')
        data = decodered(token)
        context = {
            'menu' : 'newuser',
            'email' : data['email'],
            'name': data['unique_name'],
            'role': int(data['role']),
            'login' : datetime.fromtimestamp(data['nbf']),
        }
        return render(request, 'users/newuser.html',{'datos': context})
    else: 
        return redirect('login')
    
def userdetails(request):
    if authenticated(request):
        token = request.COOKIES.get('validate')
        data = decodered(token)
        context = {
            'menu' : 'userdetails',
            'email' : data['email'],
            'name': data['unique_name'],
            'role': int(data['role']),
            'login' : datetime.fromtimestamp(data['nbf']),
        }
        return render(request, 'users/userdetails.html',{'datos': context})
    else: 
        return redirect('login')
    
#Listado de usuarios en perfil de administrador
def listusers(request):
    if authenticated(request):
        token = request.COOKIES.get('validate')
        data = decodered(token)
        headers={'Content-Type':'application/json', 'Authorization': 'Bearer '+token}
        usuarios = requests.get('http://localhost:32482/api/usuario/', headers=headers).json()
        print(usuarios['data'])
        context = {
        'menu' : 'listusers',
        'email' : data['email'],
        'name': data['unique_name'],
        'role': int(data['role']),
        'login' : datetime.fromtimestamp(data['nbf']),
        'usuarios': usuarios['data'],
        }
        return render(request, 'users/userlist.html',{'datos': context})
    else: 
        return redirect('login')

def createnewunits(request):
    token = request.COOKIES.get('validate')
    headers = {'Accept-Encoding': 'UTF-8', 'Content-Type': 'application/json', 'Accept': '*/*', 'Authorization': 'Bearer '+token}
    payload = json.dumps({
        'NombreUnidad': request.POST.get('nombreunit'),
        'DescripcionUnidad': request.POST.get('descriptunit') 
    })
    r = requests.post('http://localhost:32482/api/unidadInterna/add/', headers=headers, data=payload)
    if r.ok:

        return redirect('listunits')
    else:
        return redirect('dashboard')
    

def newunits(request):
    if authenticated(request):
        token = request.COOKIES.get('validate')
        data = decodered(token)
        context = {
        'menu' : 'newunits',
        'email' : data['email'],
        'name': data['unique_name'],
        'role': int(data['role']),
        'login' : datetime.fromtimestamp(data['nbf']),
        }
        return render(request, 'units/units.html',{'datos': context})
    else:
        return redirect('login')

def viewunits(request, id):
    if authenticated(request):
        token = request.COOKIES.get('validate')
        data = decodered(token)
        headers={'Content-Type':'application/json', 'Authorization': 'Bearer '+token}
        units = requests.get('http://localhost:32482/api/unidadInterna/', headers=headers).json()
        for i in units['data']:
            if i['idUnidadInterna'] == id:
                unidad = i
                
        context = {
        'menu' : 'viewunits',
        'email' : data['email'],
        'name': data['unique_name'],
        'role': int(data['role']),
        'login' : datetime.fromtimestamp(data['nbf']),
        'unidad': unidad,
        }
        return render(request, 'units/units.html',{'datos': context})
    else:
        return redirect('login')
    
def editunits(request, id):
    if authenticated(request):
        token = request.COOKIES.get('validate')
        data = decodered(token)
        headers={'Content-Type':'application/json', 'Authorization': 'Bearer '+token}
        units = requests.get('http://localhost:32482/api/unidadInterna/', headers=headers).json()
        for i in units['data']:
            if i['idUnidadInterna'] == id:
                unidad = i
                
        context = {
        'menu' : 'editunits',
        'email' : data['email'],
        'name': data['unique_name'],
        'role': int(data['role']),
        'login' : datetime.fromtimestamp(data['nbf']),
        'unidad': unidad,
        }
        return render(request, 'units/units.html',{'datos': context})
    else:
        return redirect('login')

def updateunits(request, id):
    if authenticated(request):
        token = request.COOKIES.get('validate')
        data = decodered(token)
        headers={'Content-Type':'application/json', 'Authorization': 'Bearer '+token}
        payload = json.dumps(
            {
        'NombreUnidad': request.POST.get('nombreunit'),
        'DescripcionUnidad': request.POST.get('descriptunit') 
        }
            )
        update = requests.put('http://localhost:32482/api/unidadInterna/update/'+str(id), headers=headers, data = payload)
        if update.ok:
            return redirect('listunits')
        else:
            return redirect('dashboard') #envia al dashboard si da error
    else:
        return redirect('login')
    
def deleteunits(request, id):
    if authenticated(request):
        token = request.COOKIES.get('validate')
        payload = json.dumps({'IdUnidadInterna': id})
        headers={'Accept-Encoding': 'UTF-8','Content-Type':'application/json','Accept': '*/*' ,'Authorization': 'Bearer '+token}
        deleted = requests.delete('http://localhost:32482/api/unidadInterna/delete/'+str(id), headers=headers)
        
        print(deleted)

        if deleted.ok:
            message  = "Eliminado correctamente"
        else:
            message = "Ocurrio un error en el proceso, favor intente nuevamente"
        
        return redirect('listunits')
    else:
        return redirect('login')

def listunits(request):
    if authenticated(request):
        token = request.COOKIES.get('validate')
        data = decodered(token)
        headers={'Accept-Encoding': 'UTF-8','Content-Type':'application/json','Accept': '*/*' ,'Authorization': 'Bearer '+token}
        units = requests.get('http://localhost:32482/api/unidadInterna/', headers=headers).json()
        
        context = {
        'menu' : 'listunits',
        'email' : data['email'],
        'name': data['unique_name'],
        'role': int(data['role']),
        'login' : datetime.fromtimestamp(data['nbf']),
        'unidades': units['data'],
        }
        return render(request, 'units/unitslist.html',{'datos': context})
    else: 
        return redirect('login')


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
