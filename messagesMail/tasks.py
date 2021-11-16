from celery.decorators import task
from celery.utils.log import get_task_logger



logger = get_task_logger(__name__)


@task(name="sendEmailTask")
def sendEmailTask(email, message):
    """sends an email when feedback form is filled successfully"""
    logger.info("Sent feedback email")
    return sendEmail(email, message)
