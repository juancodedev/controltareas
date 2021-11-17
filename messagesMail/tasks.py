from celery.schedules import crontab
from celery.decorators import task, periodic_task
from celery.utils.log import get_task_logger
from messagesMail.views import sendEmails, proximidad

logger = get_task_logger(__name__)

@task(name="sendEmailTask")
def sendEmailTask(data):
    logger.info("Sent email to users")
    return sendEmails(data)

@periodic_task(
    run_every=(crontab(hour=7, minute=30)),
    name="taskProximidad",
    ignore_result=True
)

def taskProximidad():
    proximidad()
    logger.info("Envia notificaciones de proximidad")
