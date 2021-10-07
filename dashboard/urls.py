from django.conf.urls import url
from django.contrib import admin
# from django.contrib.auth import logout
from django.urls import include, path
from dashboard import views
from login.views import logout

urlpatterns = [
    # Tareas
    path('', views.dashboard, name='dashboard'), #dashboard con resumen de tareas
    path('tasklist/', views.tasklist, name='tasklist'), #Listado de tareas
    path('tasknew/', views.tasknew, name='tasknew'), # Creacion de tarea nueva
    
    #workflow
    path('workflowlist/', views.workflowlist, name='workflowlist'), # Creacion nuevo flujo de tareas
    path('workflownew/', views.workflownew, name='workflownew'), # Creacion de tarea nueva
    path('workflowview/', views.workflowview, name='workflowview'), # Vista detalle workflow
    path('workflowhistory/', views.workflowhistory, name='workflowhistory'), # Vista detalle workflow
    
    # Equipo
    path('teamwork/', views.teamwork, name='teamwork'), # Listado de equipo de trabajo
    path('workload/', views.workload, name='workload'), # Lista la carga de trabajo por cada integrante del equipo
    path('taskdetails/', views.taskdetails, name='taskdetails'), # Detalle de la tarea asignada
    
    # Administracion
    path('newuser/', views.newuser, name='newuser'), # Creacion de usuarios
    path('newuser/createnewuser', views.createnewuser, name='createnewuser'), # Creacion de usuarios
    
    path('listusers/', views.listusers, name='listusers'), # Creacion de usuarios

    path('newunits/', views.newunits, name='newunits'), #creacion de nuevas unidades internas
    path('listunits/', views.listunits, name='listunits'), #creacion de nuevas unidades internas
    
    path('newrole/', views.newrole, name='newrole'), #creacion de nuevo rol
    path('listrole/', views.listrole, name='listrole'), #creacion de nuevas unidades internas
    
    path('admin/', views.admin, name='admin'), # Admin de django
    path('logout/', logout, name='logout'), #cierra sesion
    #rutas funcionario
    
    path('taskfuncionario/',views.taskfuncionario, name='taskfuncionario'), #lista de tareas del rol funcionario
    
    #Lista de mensajes 
    
    path('message/',views.messagelist, name='messagelist'),
    path('messagereaded/',views.messagereaded, name='messagereaded'),
    path('messageresponded/',views.messageresponded, name='messageresponded'),
    
    
    
]