from django.conf.urls import url
from django.contrib import admin
# from django.contrib.auth import logout
from django.urls import include, path
from dashboard.views import dashboard, tasklist, teamwork,admin,workload, taskdetails, tasknew,newuser,newunits,newrole,workflowlist, workflownew,listusers, listunits, listrole
from login.views import logout

urlpatterns = [
    # Tareas
    path('', dashboard, name='dashboard'), #dashboard con resumen de tareas
    path('tasklist/', tasklist, name='tasklist'), #Listado de tareas
    path('tasknew/', tasknew, name='tasknew'), # Creacion de tarea nueva
    #workflow
    path('workflowlist/', workflowlist, name='workflowlist'), # Creacion nuevo flujo de tareas
    path('workflownew/', workflownew, name='workflownew'), # Creacion de tarea nueva
    
    # Equipo
    path('teamwork/', teamwork, name='teamwork'), # Listado de equipo de trabajo
    path('workload/', workload, name='workload'), # Lista la carga de trabajo por cada integrante del equipo
    path('taskdetails/', taskdetails, name='taskdetails'), # Detalle de la tarea asignada
    
    # Administracion
    path('newuser/', newuser, name='newuser'), # Creacion de usuarios
    path('listusers/', listusers, name='listusers'), # Creacion de usuarios

    path('newunits/', newunits, name='newunits'), #creacion de nuevas unidades internas
    path('listunits/', listunits, name='listunits'), #creacion de nuevas unidades internas
    
    path('newrole/', newrole, name='newrole'), #creacion de nuevo rol
    path('listrole/', listrole, name='listrole'), #creacion de nuevas unidades internas
    
    path('admin/', admin, name='admin'), # Admin de django
    path('logout/',logout, name='logout'), #cierra sesion
    
    
]