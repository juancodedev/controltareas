from celery.decorators import task
from celery.utils.log import get_task_logger
from messagesMail.views import sendEmails

logger = get_task_logger(__name__)

@task(name="sendEmailTask")
def sendEmailTask(data):
    logger.info("Sent email to users")
    return sendEmails(data)
