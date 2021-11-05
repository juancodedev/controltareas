import json
from django.http.request import HttpHeaders
from django.shortcuts import render, redirect
from django.http import HttpResponse
from requests.api import delete, head, request
from login.views import authenticated, decodered
import requests, jwt, json
from datetime import datetime

#modulos extras solo para pruebas
import random

def imgprofiletemp(largo):
    # profile/0-41.jpg
    img={}
    img['results']=[]
    for i in range(largo):
        numero = random.randint(0,41)
        img['results'].append({
            'picture': {
            'large': str(numero)+'.jpg',
                }  
                    }
        )
    return img

def dashboard(request):
    if authenticated(request):
        token = request.COOKIES.get('validate')
        data = decodered(token)
        rol = data['role']
        if int(rol) == 1:
            headers={'Content-Type':'application/json', 'Authorization': 'Bearer '+token}
            dataAPI = requests.get('http://localhost:32482/api/usuario/', headers=headers).json()
            img = imgprofiletemp(len(dataAPI['data']))# imagenes de perfil random tomadas desde el static
            mylist = zip(dataAPI['data'],img['results']) #Se unen las listas de imagenes random + datos de usuario y se envian al template para mostrarlos

            context = {
                    'menu' : 'dashboard',
                    'email' : data['email'],
                    'name': data['unique_name'],
                    'role': int(data['role']),
                    'login' : datetime.fromtimestamp(data['nbf']),

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
        headers = {'Accept-Encoding': 'UTF-8', 'Content-Type': 'application/json', 'Accept': '*/*', 'Authorization': 'Bearer '+token}
        tareas = requests.get('http://localhost:32482/api/tarea/', headers=headers ).json()
        usuarios = requests.get('http://localhost:32482/api/usuario/', headers=headers).json()
        
        context = {
            'menu' : 'tableTask',
            'email' : data['email'],
            'name': data['unique_name'],
            'role': int(data['role']),
            'login' : datetime.fromtimestamp(data['nbf']),
            'tk': tareas['data'],
            'usuarios': usuarios['data']
        }
        return render(request, 'task/tasklist.html',{'datos': context})
    else: 
        return redirect('login')
    



def taskdelete(request, id):
    if authenticated(request):
        token = request.COOKIES.get('validate')
        headers = {'Accept-Encoding': 'UTF-8', 'Content-Type': 'application/json', 'Accept': '*/*', 'Authorization': 'Bearer '+token}
        deleted = requests.delete('http://localhost:32482/api/tarea/delete/'+str(id), headers=headers)
        
        print(deleted.status_code)
        if deleted.ok:
            message  = "Eliminado correctamente"
        else:
            message = "Ocurrio un error en el proceso, favor intente nuevamente"
        
        return redirect('tasklist')
    else: 
        return redirect('login')


def taskedit(request, id):
    if authenticated(request):
        token = request.COOKIES.get('validate')
        data = decodered(token)
        headers = {'Accept-Encoding': 'UTF-8', 'Content-Type': 'application/json', 'Accept': '*/*', 'Authorization': 'Bearer '+token}
        tareas = requests.get('http://localhost:32482/api/tarea/', headers=headers ).json()
        usuarios = requests.get('http://localhost:32482/api/usuario/', headers=headers).json()
        actividad = requests.get('http://localhost:32482/api/tarea/', headers=headers).json()
        prioridad = requests.get('http://localhost:32482/api/prioridadTarea', headers=headers).json()
        estado = requests.get('http://localhost:32482/api/estadoTarea', headers=headers).json()
        creadopor = requests.get('http://localhost:32482/api/usuario', headers=headers).json()
        justificacion = requests.get('http://localhost:32482/api/justificacionTarea/', headers=headers).json()
        tarea = list(e for e in tareas['data'] if e['idTarea']  == int(id))[0]
        
        context = {
        'menu' : 'taskedit',
        'email' : data['email'],
        'name': data['unique_name'],
        'role': int(data['role']),
        'login' : datetime.fromtimestamp(data['nbf']),
        'tareas' : tarea,
        'usuarios': usuarios['data'],
        'prioridad': prioridad['data'],
        'estado': estado['data'],
        'creadopor': creadopor['data'],
        'justificacion': justificacion['data'],
        }
        return render(request, 'task/task.html',{'datos': context})
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
def taskdetails(request, id):
    if authenticated(request):
        token = request.COOKIES.get('validate')
        data = decodered(token)
        headers = {'Accept-Encoding': 'UTF-8', 'Content-Type': 'application/json', 'Accept': '*/*', 'Authorization': 'Bearer '+token}
        tareas = requests.get('http://localhost:32482/api/tarea/', headers=headers ).json()
        usuarios = requests.get('http://localhost:32482/api/usuario/', headers=headers).json()
        actividad = requests.get('http://localhost:32482/api/tarea/', headers=headers).json()
        
        
        context = {
            'menu' : 'taskdetails',
            'email' : data['email'],
            'name': data['unique_name'],
            'role': int(data['role']),
            'login' : datetime.fromtimestamp(data['nbf']),
            'tareas': list(e for e in tareas['data'] if e['idTarea']  == int(id))[0],
            'usuarios': usuarios['data'],
            'actividad': actividad['data'],
        }
        return render(request, 'task/taskdetails.html',{'datos': context})
    else: 
        return redirect('login')
    
#Creacion de tareas renderizado del template
def tasknew(request):
    if authenticated(request):
        token = request.COOKIES.get('validate')
        data = decodered(token)
        headers = {'Accept-Encoding': 'UTF-8', 'Content-Type': 'application/json', 'Accept': '*/*', 'Authorization': 'Bearer '+token}
        usuarios = requests.get('http://localhost:32482/api/usuario/', headers=headers).json()
        prioridad = requests.get('http://localhost:32482/api/prioridadTarea', headers=headers).json()
        estado = requests.get('http://localhost:32482/api/estadoTarea', headers=headers).json()
        creadopor = requests.get('http://localhost:32482/api/usuario', headers=headers).json()
                
        context = {
            'menu' : 'tasknew',
            'email' : data['email'],
            'name': data['unique_name'],
            'role': int(data['role']),
            'login' : datetime.fromtimestamp(data['nbf']),
            'usuarios': usuarios['data'],
            'prioridad': prioridad['data'],
            'estado': estado['data'],
            'creadopor': creadopor['data'],
        }
        return render(request, 'task/task.html',{'datos': context})
    else: 
        return redirect('login')


def updatetask(request, id):
    if authenticated(request):
        token = request.COOKIES.get('validate')
        headers={'Content-Type':'application/json', 'Authorization': 'Bearer '+token}


        payload = json.dumps(
        {
            'idTarea': id,
            'nombreTarea':request.POST.get('nombretarea'),
            'descripcionTarea': request.POST.get('descripciontarea'),
            'fechaPlazo': request.POST.get('fechaplazo'),
            'fkRutUsuario' : request.POST.get('creadopor'),
            'fkEstadoTarea': int(request.POST.get('estadotarea')),
            'fkPrioridadTarea' : int(request.POST.get('prioridadtarea')),
        })
        update = requests.put('http://localhost:32482/api/tarea/update/'+str(id), headers=headers, data = payload)
        print(update)
        print(payload)
        if update.ok: 
            return redirect('tasklist')
        else:
            return redirect('dashboard') #envia al dashboard si da error
    else:
        return redirect('login')

#Salvar datos de la nueva tarea
def savenewtask(request):
    if authenticated(request):
        token = request.COOKIES.get('validate')
        headers = {'Accept-Encoding': 'UTF-8', 'Content-Type': 'application/json', 'Accept': '*/*', 'Authorization': 'Bearer '+token}
        
        fecha = request.POST.get('fechaplazo')
        print(fecha)
        payload = json.dumps({
            'nombreTarea':request.POST.get('nombretarea'),
            'descripcionTarea': request.POST.get('descripciontarea'),
            'fechaPlazo': request.POST.get('fechaplazo'),
            
            'reporteProblema': 'Ninguno',
            
            'asignacionTarea': request.POST.get('asignadoa'),
            'fkRutUsuario' : request.POST.get('creadopor'),
            
            'fkEstadoTarea' : int(1),
            'fkPrioridadTarea' : int(request.POST.get('prioridadtarea')),

        })
        r = requests.post('http://localhost:32482/api/tarea/add', headers=headers, data=payload)

        if r.ok:
            print('Tarea creado correctamente')
            print(r.status_code)
        else:
            print('Error')
            print(r.status_code)


        return redirect('tasklist')
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
        headers={'Content-Type':'application/json', 'Authorization': 'Bearer '+token}
        rol = requests.get('http://localhost:32482/api/rol/', headers=headers).json()
        unidades = requests.get('http://localhost:32482/api/unidadInterna/', headers=headers).json()
        context = {
            'menu' : 'newuser',
            'email' : data['email'],
            'name': data['unique_name'],
            'role': int(data['role']),
            'login' : datetime.fromtimestamp(data['nbf']),
            'unidad': unidades['data'],
            'rol': rol['data'],
        }
        return render(request, 'users/newuser.html',{'datos': context})
    else: 
        return redirect('login')

#Listo los datos del usuario existente
def viewusers(request, id):
    if authenticated(request):
        token = request.COOKIES.get('validate')
        data = decodered(token)
        headers={'Content-Type':'application/json', 'Authorization': 'Bearer '+token}
        user = requests.get('http://localhost:32482/api/usuario/oneUser/'+str(id), headers=headers).json()
        
        context = {
            'menu' : 'viewusers',
            'email' : data['email'],
            'name': data['unique_name'],
            'role': int(data['role']),
            'login': datetime.fromtimestamp(data['nbf']),
            'user': user['data'][0],
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

def editusers(request, id):
    if authenticated(request):
        token = request.COOKIES.get('validate')
        data = decodered(token)
        headers={'Content-Type':'application/json', 'Authorization': 'Bearer '+token}
        user = requests.get('http://localhost:32482/api/usuario/oneUser/'+str(id), headers=headers).json()
        rol = requests.get('http://localhost:32482/api/rol/', headers=headers).json()
        unidades = requests.get('http://localhost:32482/api/unidadInterna/', headers=headers).json()
        
        context = {
        'menu' : 'editusers',
        'email' : data['email'],
        'name': data['unique_name'],
        'role': int(data['role']),
        'login' : datetime.fromtimestamp(data['nbf']),
        'user': user['data'][0],
        'unidad': unidades['data'],
        'rol': rol['data'],
        }
        return render(request, 'users/newuser.html',{'datos': context})
    else:
        return redirect('login')

def deleteusers(request, id):
    if authenticated(request):
        token = request.COOKIES.get('validate')
        payload = json.dumps({'IdUnidadInterna': id})
        headers={'Accept-Encoding': 'UTF-8','Content-Type':'application/json','Accept': '*/*' ,'Authorization': 'Bearer '+token}
        deleted = requests.delete('http://localhost:32482/api/usuario/delete/'+str(id), headers=headers)
        if deleted.ok:
            message  = "Eliminado correctamente"
        else:
            message = "Ocurrio un error en el proceso, favor intente nuevamente"
        
        return redirect('listusers')
    else:
        return redirect('login')


def updateusers(request, id):
    if authenticated(request):
        token = request.COOKIES.get('validate')
        data = decodered(token)
        headers={'Content-Type':'application/json', 'Authorization': 'Bearer '+token}
        payload = json.dumps(
            {
            'rutUsuario': request.POST.get('rut'),
            'nombreUsuario': request.POST.get('name'),
            'segundoNombre': request.POST.get('secondName'),
            'apellidoUsuario': request.POST.get('lastName'),
            'segundoApellido': request.POST.get('secondlastName'),
            'correoElectronico': request.POST.get('email'),
            'numTelefono': int(request.POST.get('phoneNumber')),
            'idRolUsuario': int(request.POST.get('role')),
            'idUnidadInternaUsuario': int(request.POST.get('unidadInterna'))
        }
            )
        update = requests.put('http://localhost:32482/api/usuario/update/'+str(id), headers=headers, data = payload)
        if update.ok:
            return redirect('listusers')
        else:
            return redirect('dashboard') #envia al dashboard si da error
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
    if authenticated(request):
        token = request.COOKIES.get('validate')
        data = decodered(token)
        
        context = {
        'menu' : 'newrole',
        'email' : data['email'],
        'name': data['unique_name'],
        'role': int(data['role']),
        'login' : datetime.fromtimestamp(data['nbf']),
        }
        return render(request, 'role/role.html',{'datos': context})
    else:
        return redirect('login')

def viewrole(request, id):
    if authenticated(request):
        token = request.COOKIES.get('validate')
        data = decodered(token)
        headers={'Content-Type':'application/json', 'Authorization': 'Bearer '+token}
        rollist = requests.get('http://localhost:32482/api/rol/', headers=headers).json()
        print(rollist)
        for i in rollist['data']:
            if i['rolId'] == id:
                rol = i
        print(rol) 
        context = {
        'menu' : 'viewrole',
        'email' : data['email'],
        'name': data['unique_name'],
        'role': int(data['role']),
        'login' : datetime.fromtimestamp(data['nbf']),
        'rollist': rol,
        }
        return render(request, 'role/role.html',{'datos': context})
    else:
        return redirect('login')


def editrole(request, id):
    if authenticated(request):
        token = request.COOKIES.get('validate')
        data = decodered(token)
        headers={'Content-Type':'application/json', 'Authorization': 'Bearer '+token}
        rollist = requests.get('http://localhost:32482/api/rol/', headers=headers).json()
        print(rollist)
        for i in rollist['data']:
            if i['rolId'] == id:
                rol = i
        print(rol) 
                
        context = {
        'menu' : 'editrole',
        'email' : data['email'],
        'name': data['unique_name'],
        'role': int(data['role']),
        'login' : datetime.fromtimestamp(data['nbf']),
        'rollist': rol,
        }
        return render(request, 'role/role.html',{'datos': context})
    else:
        return redirect('login')

def updaterole(request, id):
    if authenticated(request):
        token = request.COOKIES.get('validate')
        headers={'Content-Type':'application/json', 'Authorization': 'Bearer '+token}
        payload = json.dumps(
            {
        'nombreRol': request.POST.get('nombrerol'),
        'DescripcionRol': request.POST.get('descriptrole') 
        }
            )
        update = requests.put('http://localhost:32482/api/rol/update/'+str(id), headers=headers, data = payload)
        if update.ok:
            return redirect('listrole')
        else:
            return redirect('dashboard') #envia al dashboard si da error
    else:
        return redirect('login')
    
def deleterole(request, id):
    if authenticated(request):
        token = request.COOKIES.get('validate')
        headers={'Accept-Encoding': 'UTF-8','Content-Type':'application/json','Accept': '*/*' ,'Authorization': 'Bearer '+token}
        deleted = requests.delete('http://localhost:32482/api/rol/delete/'+str(id), headers=headers)

        if deleted.ok:
            message  = "Eliminado correctamente"
        else:
            message = "Ocurrio un error en el proceso, favor intente nuevamente"
        
        return redirect('listrole')
    else:
        return redirect('login')

def listrole(request):
    if authenticated(request):
        token = request.COOKIES.get('validate')
        data = decodered(token)
        headers={'Accept-Encoding': 'UTF-8','Content-Type':'application/json','Accept': '*/*' ,'Authorization': 'Bearer '+token}
        roles = requests.get('http://localhost:32482/api/rol/', headers=headers).json()
        context = {
        'menu' : 'listrole',
        'email' : data['email'],
        'name': data['unique_name'],
        'role': int(data['role']),
        'login' : datetime.fromtimestamp(data['nbf']),
        'roles': roles['data'],
        }
        return render(request, 'role/rolelist.html',{'datos': context})
    else: 
        return redirect('login')

def createnewrole(request):
    token = request.COOKIES.get('validate')
    headers = {'Accept-Encoding': 'UTF-8', 'Content-Type': 'application/json', 'Accept': '*/*', 'Authorization': 'Bearer '+token}
    payload = json.dumps({
        'nombreRol': request.POST.get('nombrerol'),
        'DescripcionRol': request.POST.get('descriptrole') 
    })
    r = requests.post('http://localhost:32482/api/rol/add/', headers=headers, data=payload)
    if r.ok:

        return redirect('listrole')
    else:
        return redirect('dashboard')
    



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


#Metodos para perfil funcionario

def taskfuncionario(request):
    if authenticated(request):
        token = request.COOKIES.get('validate')
        data = decodered(token)
        headers = {'Accept-Encoding': 'UTF-8', 'Content-Type': 'application/json', 'Accept': '*/*', 'Authorization': 'Bearer '+token}
        tareas = requests.get('http://localhost:32482/api/tarea/', headers=headers ).json()
        usuarios = requests.get('http://localhost:32482/api/usuario/', headers=headers).json()
        tareasf = list(e for e in tareas['data'] if e['fkRutUsuario']  == data['nameid'] and e['fkEstadoTarea'] == 2 )

        context = {
        'menu' : 'taskfuncionario',
        'email' : data['email'],
        'name': data['unique_name'],
        'role': int(data['role']),
        'login' : datetime.fromtimestamp(data['nbf']),
        'tk': tareasf,
        'usuarios': usuarios['data']
        }
        return render(request, 'task/tasklist.html',{'datos': context})
    else: 
        return redirect('login')

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

# DENNISSE SECTION

#Creacion de tareas subordinada renderizado del template
def TareaSubordinadaSection(request):
    if authenticated(request):
        # Return Section
        token = request.COOKIES.get('validate')
        data = decodered(token)
        headers = {'Content-Type':'application/json', 'Authorization': 'Bearer '+ token}
        dataAPI = requests.get('http://localhost:32482/api/TareaSubordinada', headers=headers).json()
        listTareaSubordinada = dataAPI['data']

        # Variables con data a enviar a la vista
        
        context = {
            'menu' : 'TareaSubordinadaSection',
            'email' : data['email'],
            'name': data['unique_name'],
            'role': int(data['role']),
            'login' : datetime.fromtimestamp(data['nbf']),
            'tareaSubordinada': listTareaSubordinada
        }
        return render(request, 'subordinatetask/list_subordinatetask.html', {'data': context})
    else: 
        return redirect('login')

def AddTareaSubordinadaSection(request):
    if authenticated(request):
        # Consumo de API: Tarea 
        # Method: GET
        token = request.COOKIES.get('validate')
        headers = {'Content-Type':'application/json', 'Authorization': 'Bearer '+ token}
        resTarea = requests.get('http://localhost:32482/api/tarea', headers=headers)
        dataTarea = resTarea.json()
        listTarea = dataTarea['data']

        # Consumo de API: Prioridad Tarea
        # Method: GET
        resPrioridad = requests.get('http://localhost:32482/api/prioridadTarea', headers=headers)
        dataPrioridad = resPrioridad.json()
        listPrioridad = dataPrioridad['data']

        # Consumo de API: Estado Tarea
        # Method: GET
        resEstado = requests.get('http://localhost:32482/api/estadoTarea', headers=headers)
        dataEstado = resEstado.json()
        listEstado = dataEstado['data']

        # Consumo de API: Tarea Subordinada
        nombre = request.POST.get('nombreTareaSubordinada')
        descripcion = request.POST.get('descripcionTareaSubordinada')
        prioridadFk = request.POST.get('selectPrioridadTarea')
        estadoFk = 1
        tareaFk = request.POST.get('selectTarea')

        status = ''
        if nombre == '' or descripcion == '' or prioridadFk == '' or estadoFk == '' or tareaFk == '' or nombre == None:
            status = 'ERROR'
        elif nombre != '' or descripcion != '' or prioridadFk != '' or estadoFk != '' or tareaFk != '' or nombre != None:
            status = 'OK'
        else: 
            status
        
        if status == 'OK':
            AddTareaSubordinada(request, nombre, descripcion, prioridadFk, estadoFk, tareaFk)

        # Variables con data para enviar a la vista
        context = {
            'tarea': listTarea,
            'prioridad': listPrioridad,
            'estado': listEstado,
            'statusCreation': status,
            'listPrioridadTarea': listPrioridad
        }

        # Return Section
        return render(request, 'subordinatetask/subordinatetask.html', {'data': context})
    
    else: 
        return redirect('login')

def DeleteTareaSubordinadaSection(request, idTareaSub):
    if authenticated:
        status = 'NO_CONTENT'
        token = request.COOKIES.get('validate')
        headers = {'Accept-Encoding': 'UTF-8', 'Content-Type': 'application/json', 'Authorization': 'Bearer '+ token,'Accept': '*/*' }

        # Consumo de API: Tarea Subordinada
        # Method: DELETE
        tareaSub = str(idTareaSub)
        payload = json.dumps({'idTareaSubordinada': tareaSub})
        r = requests.delete('http://localhost:32482/api/TareaSubordinada/delete/' + tareaSub, headers=headers, data=payload)
        print(r)

        # Consumo de API: Tarea Subordinada
        # Method: GET
        reqTareaSubordinada = requests.get('http://localhost:32482/api/TareaSubordinada', headers=headers)
        dataAPI = reqTareaSubordinada.json()
        listTareaSubordinada = dataAPI['data']

        context = {
            'tareaSubordinada': listTareaSubordinada,
            'deleteStatus': status
        }

        if r.ok:
            status = 'DELETED'
            print(status)
            return redirect('TareaSubordinadaSection')
        else: 
            status = 'ERROR'
            print(status)
            return render(request, 'subordinatetask/list_subordinatetask.html', {'data': context})
        
    else:
        return redirect('login')

def EditTareaSubordinadaSection(request, idTareaSub):
    if authenticated:

        # Configuración Header
        status = 'NO_CONTENT'
        token = request.COOKIES.get('validate')
        headers = {'Accept-Encoding': 'UTF-8', 'Content-Type': 'application/json', 'Authorization': 'Bearer '+ token,'Accept': '*/*' }

        # Consumo de API: Tarea
        # Method: GET
        resTarea = requests.get('http://localhost:32482/api/tarea', headers=headers)
        dataTarea = resTarea.json()
        listTarea = dataTarea['data']

        # Consumo de API: OneTareaSubordinada
        # Method: GET with Params
        tareaSub = str(idTareaSub)
        resOneTareaSub = requests.get('http://localhost:32482/api/TareaSubordinada/oneTareaSubordinada/'+ tareaSub, headers=headers)
        dataTareaSub = resOneTareaSub.json()
        OneTareaSubordinada = dataTareaSub['data']

        # Consumo de API: Estado Tarea
        # Method: GET
        resEstado = requests.get('http://localhost:32482/api/estadoTarea', headers=headers)
        dataEstado = resEstado.json()
        listEstado = dataEstado['data']

        # Consumo de API: Prioridad Tarea
        # Method: GET
        resPrioridad = requests.get('http://localhost:32482/api/prioridadTarea', headers=headers)
        dataPrioridad = resPrioridad.json()
        listPrioridad = dataPrioridad['data']

        # Asignación del ID de Tarea Subordinada a Buscar
        idTareaSubordinadaToSearch = ''
        for x in OneTareaSubordinada:
            idTareaSubordinadaToSearch = x['idTareaSubordinada']
           # print(idTareaSubordinadaToSearch)

        # Validate Data Extraction
        if request.method == 'POST':
            try:
                #Recuperación de data proveniente del HTML
                nombre = request.POST.get('nombreTareaSubordinada')
                descripcion = request.POST.get('descripcionTareaSubordinada')
                prioridadFk = request.POST.get('prioridadtarea')
                estadoFk = request.POST.get('estadoTarea')
                tareaFk = request.POST.get('selectTarea')
                status = 'OK'
                #print(nombre, descripcion, tareaFk)
            except:
                status = 'ERROR'

        # Método Update User
        try:
            if status == 'OK':
                EditTareaSubordinada(request, nombre, descripcion, prioridadFk, estadoFk, tareaFk, idTareaSubordinadaToSearch)
            
        except:
            status = 'ERROR'
        
        context = {
            'tarea': listTarea,
            'statusUpdate': status,
            'oneTareaSubordinada': OneTareaSubordinada,
            'listPrioridadTarea': listPrioridad,
            'listEstadoTarea':listEstado,
        }

        # Return Section
        return render(request, 'subordinatetask/updatesubordinatetask.html', {'data':context})

    else:
        return redirect('login')



# Métodos Complementarios
# --------------------------------------------
# CRUD: Tarea Subordinada

# METHOD: POST
def AddTareaSubordinada(request, nombre, descripcion, prioridadFk, estadoFk, tareaFk):
    if authenticated:
        token = request.COOKIES.get('validate')
        headers = {'Accept-Encoding': 'UTF-8', 'Content-Type': 'application/json', 'Authorization': 'Bearer '+token, 'Accept': '*/*' }

        # Datos a enviar a la petición POST
        payload = json.dumps({'nombreSubordinada' : nombre,
                              'descripcionSubordinada': descripcion,
                              'fkPrioridadTarea': int(prioridadFk),
                              'fkEstadoTarea': int(estadoFk),
                              'fkIdTarea': int(tareaFk),
        })
        r = requests.post('http://localhost:32482/api/TareaSubordinada/add', headers=headers, data=payload)

# METHOD: PUT
def EditTareaSubordinada(request, nombre, descripcion, prioridadFk, estadoFk, tareaFk, idTareaSubordinadaToSearch):
    if authenticated:
        token = request.COOKIES.get('validate')
        headers = {'Accept-Encoding': 'UTF-8', 'Content-Type': 'application/json', 'Authorization': 'Bearer '+ token,'Accept': '*/*' }


        # Datos a enviar a la petición PUT
        payload = json.dumps({'nombreSubordinada' : nombre,
                              'descripcionSubordinada': descripcion,
                              'fkPrioridadTarea': int(prioridadFk),
                              'fkEstadoTarea': int(estadoFk),
                              'fkIdTarea': int(tareaFk),
        })
        r = requests.put('http://localhost:32482/api/TareaSubordinada/update/' + str(idTareaSubordinadaToSearch), headers=headers, data=payload)


# Método para Aceptar Tareas
def AcceptTask(request, idTask):
    if authenticated:
        try:
            token = request.COOKIES.get('validate')
            headers = {'Accept-Encoding': 'UTF-8', 'Content-Type': 'application/json', 'Authorization': 'Bearer '+ token,'Accept': '*/*' }
            reqAcceptTask = requests.put('http://localhost:32482/api/tarea/acceptTask/' + idTask, headers=headers)
            print(reqAcceptTask)
            return redirect('taskfuncionario')

        except:
            print('ERROR')
    
    else: 
        redirect('login')


# Metodo Rechazar

def RejectTask(request, idTask):
    if authenticated:
        token = request.COOKIES.get('validate')
        headers = {'Accept-Encoding': 'UTF-8', 'Content-Type': 'application/json', 'Authorization': 'Bearer '+ token,'Accept': '*/*' }
        
        try:
            descripcion = request.POST.get('descripcion')
            print(descripcion)
            status = ''
            if descripcion == '':
                status = 'ERROR'
            elif descripcion != '':
                status = 'OK'
            else:
                status
            if  status == 'OK':
                Addjustificacion(request,descripcion,idTask)

            return redirect('taskfuncionario')

        except:
            print('ERROR')
            return redirect('taskfuncionario')
    
    else: 
        redirect('login')


def Addjustificacion(request,description,idTask):
    if authenticated:
        token = request.COOKIES.get('validate')
        headers = {'Accept-Encoding': 'UTF-8', 'Content-Type': 'application/json', 'Authorization': 'Bearer '+ token,'Accept': '*/*' }


        # Datos a enviar a la petición POST
        payload = json.dumps({
                                'Descripcion': description,
        })
        r = requests.post('http://localhost:32482/api/justificacionTarea/add/' + idTask, headers=headers, data=payload)

# DENNISSE SECTION

