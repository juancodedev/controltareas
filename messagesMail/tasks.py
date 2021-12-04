from datetime import datetime
import json, requests, jwt
from controltareas.settings import API


from celery.schedules import crontab
from celery.decorators import task, periodic_task
from celery.utils.log import get_task_logger
from messagesMail.views import sendEmails

logger = get_task_logger(__name__)

@task(name="sendEmailTask")
def sendEmailTask(data):
    if data['evento'] == 'Tarea Rechazada':
        logger.info("Sent email --> Tarea rechazada")
    elif data['evento'] == 'Actualizacion de tarea':
        logger.info("Sent email --> Actualizacion de tarea")
    elif data['evento'] == 'Finalización de tarea':
        logger.info("Sent email --> Finalización de tarea")
    elif data['evento'] == 'Alerta de priximidad':
        logger.info("Sent email --> Envio de notificaciones")
    elif data['evento'] == 'Reporte Problema':
        logger.info("Sent email --> Reporte Problema")
    return sendEmails(data)

# @periodic_task(
#     run_every=(crontab(hour=7, minute=30)),
#     name="taskProximidad",
#     ignore_result=True
# )


@periodic_task(
    run_every=(crontab(hour=7, minute=30)),
    name="taskProximidad",
    ignore_result=True
)

def taskProximidad():
    logger.info("Enviando notificaciones de proximidad")
    
    payload = json.dumps({'email': 'admin@admintask.com', 'password': 'olidata123'})
    headers = {'Accept-Encoding': 'UTF-8', 'Content-Type': 'application/json', 'Accept': '*/*'}
    tokenAPI = requests.post(API+'login/addlogin/', headers=headers, data=payload).json()
    headersToken = {'Accept-Encoding': 'UTF-8', 'Content-Type': 'application/json', 'Accept': '*/*', 'Authorization': 'Bearer '+tokenAPI['data']['token']}        
    tareasNotificar = requests.get(API+'tarea/getNotificarionTask', headers=headersToken).json()
    usuarios = requests.get(API+'usuario/', headers=headersToken).json()

    for tarea in tareasNotificar['data']:
        data = {
            'evento': 'Notificacion de Tarea',
            'user': list(e for e in usuarios['data'] if e['rutUsuario']  == tarea['fkRutUsuario'])[0]['nombreUsuario']+' '+list(e for e in usuarios['data'] if e['rutUsuario']  == tarea['fkRutUsuario'])[0]['apellidoUsuario'],
            'email': list(e for e in usuarios['data'] if e['rutUsuario']  == tarea['fkRutUsuario'])[0]['correoElectronico'],
            'tarea': tarea,
            'vence': ((datetime.strptime(tarea['fechaPlazo'],'%Y-%m-%dT%H:%M:%S')-datetime.now()).days)+1,
            }
        sendEmails(data)
    
@periodic_task(
    run_every=(crontab(hour=9, minute=55)),
    name="taskProgress",
    ignore_result=True
)
def taskProgress():
    logger.info("Procesando tareas Atrasadas")
    payload = json.dumps({'email': 'admin@admintask.com', 'password': 'olidata123'})
    headers = {'Accept-Encoding': 'UTF-8', 'Content-Type': 'application/json', 'Accept': '*/*'}
    tokenAPI = requests.post(API+'login/addlogin/', headers=headers, data=payload).json()
    headersToken = {'Accept-Encoding': 'UTF-8', 'Content-Type': 'application/json', 'Accept': '*/*', 'Authorization': 'Bearer '+tokenAPI['data']['token']}        
    overDueTask = requests.post(API+'tarea/listenToDelayedTask/', headers=headersToken)
    
    if overDueTask.ok:
        logger.info("Proceso tareas Atrasadas concluido")
    return None