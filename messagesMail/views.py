from django.http import request
from django.shortcuts import redirect, render
from controltareas.settings import EMAIL_HOST, EMAIL_PORT, EMAIL_HOST_USER, EMAIL_HOST_PASSWORD
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from django.template.loader import render_to_string
import smtplib, ssl
import celery

def testmail( data):
    context = {
            'evento': data['evento'], 
            'user': data['user'],
            'tarea': data['tarea'],
            'prioridad': data['prioridad']
        }
    return render('email/email.html',context)

def sendEmails(data):
    try:
        mailServer = smtplib.SMTP(EMAIL_HOST, EMAIL_PORT)
        print(mailServer.ehlo())
        mailServer.starttls()
        print(mailServer.ehlo())
        mailServer.login(EMAIL_HOST_USER,EMAIL_HOST_PASSWORD)
        
        email_to = data['email']
        # Construimos el mensaje simple
        mensaje = MIMEMultipart()
        mensaje['From'] = EMAIL_HOST_USER
        mensaje['To'] = email_to
        mensaje['Subject'] = "Sistema de notificaciones de tareas"
        
        context = {
            'evento': data['evento'],
            'user': data['user'],
            'tarea': data['tarea'],
            'prioridad': data['prioridad'],
            }
        
        content = render_to_string('email/email.html', context)
        mensaje.attach(MIMEText(content, 'html'))

        mailServer.sendmail(EMAIL_HOST_USER,
                            email_to,
                            mensaje.as_string())
        # Cierre de la conexion
        mailServer.close()

    except Exception as e:
        print(e)

@celery.task
def proximidad():
    print("algo") 
        
