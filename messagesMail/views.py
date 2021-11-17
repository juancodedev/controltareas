from django.shortcuts import redirect, render
from controltareas.settings import EMAIL_HOST, EMAIL_PORT, EMAIL_HOST_USER, EMAIL_HOST_PASSWORD
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from django.template.loader import render_to_string
import smtplib, ssl
from django.http.request import HttpRequest

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
            'user': data['user'],
            'tarea': data['tarea'],
            'fechaPlazo': data['fechaPlazo'],
            'prioridad': data['prioridad'],
            'descripcion': data['descripcion'],
            }
        
        content = render_to_string('email/email.html', context)
        mensaje.attach(MIMEText(content, 'html'))

        mailServer.sendmail(EMAIL_HOST_USER,
                            email_to,
                            mensaje.as_string())
        # Cierre de la conexion
        mailServer.close()
        
        # message = """\
        #     Subject: Hola { "data['user']" }

        #     This message is sent from Python."""
        
        # receiver_email = 'cl.jmunoz@gmail.com'
        # context = ssl.create_default_context()
        # with smtplib.SMTP_SSL(EMAIL_HOST, 465, context=context) as server:
        #     server.login(EMAIL_HOST_USER, EMAIL_HOST_PASSWORD)
        #     server.sendmail(EMAIL_HOST_USER, receiver_email, message)
    except Exception as e:
        print(e)
        
        
        
def testmail(request):
    context = {
            'user': 'juan muñoz',
            'tarea': int(432),
            'fechaPlazo': '20/12/203333',
            'prioridad': 'alta',
            'descripcion': 'coso',
        }
    
    return render(request, 'email/email.html',context)