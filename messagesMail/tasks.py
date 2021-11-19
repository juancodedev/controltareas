from celery.schedules import crontab
from celery.decorators import task, periodic_task
from celery.utils.log import get_task_logger
from messagesMail.views import sendEmails, proximidad

logger = get_task_logger(__name__)

@task(name="sendEmailTask")
def sendEmailTask(data):
    if data['evento'] == 'Tarea Rechazada':
        logger.info("Sent email --> Tarea rechazada")
    elif data['evento'] == 'Actualizacion de tarea':
        logger.info("Sent email --> Actualizacion de tarea")

    
    return sendEmails(data)

@periodic_task(
    run_every=(crontab(hour=7, minute=30)),
    name="taskProximidad",
    ignore_result=True
)

def taskProximidad():
    proximidad()
    logger.info("Envia notificaciones de proximidad")
