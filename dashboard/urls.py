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
    path('tasknew/', views.tasknew, name='tasknew'), # renderizado de formulario de tarea nueva
    path('updatetask/<int:id>', views.updatetask, name='updatetask'), # Guardar tarea nueva
    path('taskedit/<int:id>', views.taskedit, name='taskedit'), # Guardar tarea nueva
    path('savenewtask/', views.savenewtask, name='savenewtask'), # Guardar tarea nueva
    path('taskcomplete/<int:idTask>', views.taskcomplete, name="taskcomplete"), # Completa las tareas
    

    path('taskdetails/<int:id>', views.taskdetails, name='taskdetails'), # Guardar tarea nueva
    path('taskdelete/<int:id>', views.taskdelete, name='taskdelete'), # Guardar tarea nueva

    
    
    #workflow
    path('workflowlist/', views.workflowlist, name='workflowlist'), # Creacion nuevo flujo de tareas
    path('workflownew/', views.workflownew, name='workflownew'), # Creacion de tarea nueva
    path('workflowview/', views.workflowview, name='workflowview'), # Vista detalle workflow
    path('workflowhistory/', views.workflowhistory, name='workflowhistory'), # Vista detalle workflow
    
    # Equipo
    path('teamwork/', views.teamwork, name='teamwork'), # Listado de equipo de trabajo
    path('workload/<str:id>', views.workload, name='workload'), # Lista la carga de trabajo por cada integrante del equipo    
    # Administracion
    path('newuser/', views.newuser, name='newuser'), # Creacion de usuarios
    path('listusers/', views.listusers, name='listusers'), # Creacion de usuarios
    path('createnewuser/', views.createnewuser, name='createnewuser'), # Creacion de usuarios
    path('editusers/<str:id>', views.editusers, name='editusers'), #editar usuarios
    path('viewusers/<str:id>', views.viewusers, name='viewusers'), #Ver usuarios

    
    path('deleteusers/<str:id>', views.deleteusers, name='deleteusers'), #editar nuevas unidades internas
    path('updateusers/<str:id>', views.updateusers, name='updateusers'), #editar nuevas unidades internas


    
    

    path('newunits/', views.newunits, name='newunits'), #creacion de nuevas unidades internas
    path('viewunits/<int:id>', views.viewunits, name='viewunits'), #ver de nuevas unidades internas
    path('listunits/', views.listunits, name='listunits'), #creacion de nuevas unidades internas
    path('editunits/<int:id>', views.editunits, name='editunits'), #editar nuevas unidades internas
    path('deleteunits/<int:id>', views.deleteunits, name='deleteunits'), #editar nuevas unidades internas
    path('createnewunits/', views.createnewunits, name='createnewunits'), #editar nuevas unidades internas
    path('updateunits/<int:id>', views.updateunits, name='updateunits'), #editar nuevas unidades internas

    #grupo administrador de roles de usuarios.
    path('newrole/', views.newrole, name='newrole'), #creacion de nuevo rol
    path('listrole/', views.listrole, name='listrole'), #creacion de nuevas unidades internas
   
    path('viewrole/<int:id>', views.viewrole, name='viewrole'), #ver de nuevas unidades internas
    path('editrole/<int:id>', views.editrole, name='editrole'), #editar nuevas unidades internas
    path('deleterole/<int:id>', views.deleterole, name='deleterole'), #editar nuevas unidades internas
    path('createnewrole/', views.createnewrole, name='createnewrole'), #editar nuevas unidades internas
    path('updaterole/<int:id>', views.updaterole, name='updaterole'), #editar nuevas unidades internas

    
    
    
    # path('admin/', views.admin, name='admin'), # Admin de django
    path('logout/', logout, name='logout'), #cierra sesion
    #rutas funcionario
    
    path('taskfuncionario/',views.taskfuncionario, name='taskfuncionario'), #lista de tareas del rol funcionario
    path('acceptTask/<str:idTask>', views.AcceptTask, name="AcceptTask"),
    path('rejectTask/<str:idTask>', views.RejectTask, name="RejectTask"),

    #Lista de mensajes 
    
    path('message/',views.messagelist, name='messagelist'),
    path('messagereaded/',views.messagereaded, name='messagereaded'),
    path('messageresponded/',views.messageresponded, name='messageresponded'),
    

    #Tareas subordinadas
    path('tareaSubordinadaSection/', views.TareaSubordinadaSection, name='TareaSubordinadaSection'),
    path('addTareaSubordinadaSection/', views.AddTareaSubordinadaSection, name="AddTareaSubordinadaSection"),
    path('tareaSubordinadaSection/deleteTareaSubordinadaSection/<int:idTareaSub>', views.DeleteTareaSubordinadaSection, name="DeleteTareaSubordinadaSection"),
    path('tareaSubordinadaSection/updateTareaSubordinadaSection/<int:idTareaSub>', views.EditTareaSubordinadaSection, name="EditTareaSubordinadaSection"),

    #Empresas Alejandro
    path('empresaList/',views.EmpresasList, name='EmpresaList'),
    path('addEmpresa/',views.AddEmpresaSection, name='EmpresaAdd'),
    path('editEmpresa/<str:rutEmpresa>', views.EditEmpresaSection, name='EmpresaEdit'),
    path('empresaList/deleteEmpresaSection/<str:rutEmpresa>', views.DeleteEmpresaSection, name='deleteEmpresaSection'),
    path('viewEmpresa/<str:id>', views.ViewEmpresa, name='viewEmpresa'),
    
    path('progressTask/<str:idTask>', views.ProgressTask, name='progressTask'),
    #path('progressTask/(?P<idTask>[0-9]+)$', views.progressTask, name='progressTask'),
    
]