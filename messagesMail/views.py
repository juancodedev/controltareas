from django.http import request
from django.shortcuts import redirect, render
from controltareas.settings import EMAIL_HOST, EMAIL_PORT, EMAIL_HOST_USER, EMAIL_HOST_PASSWORD
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from django.template.loader import render_to_string
import smtplib, ssl
import celery

def testmail( data):

    print(data)
    context = {
            'evento': 'Tarea Rechazada',
            'user': 'Juan Muñoz',
            'tarea': 'Tarea 1'
        }
    return render(request, 'email/email.html',{'datos': context})

# def sendEmails(data):
#     try:
#         mailServer = smtplib.SMTP(EMAIL_HOST, EMAIL_PORT)
#         print(mailServer.ehlo())
#         mailServer.starttls()
#         print(mailServer.ehlo())
#         mailServer.login(EMAIL_HOST_USER,EMAIL_HOST_PASSWORD)

#         # Construimos el mensaje simple
#         mensaje = MIMEMultipart()
#         mensaje['From'] =  "Sistema de Notificaciones AdminTask"

#         mensaje['To'] = data['email']

#         mensaje['Subject'] = "Sistema de notificaciones de tareas"
#         destinatarios = []



#         content = render_to_string('email/email.html', context)
#         mensaje.attach(MIMEText(content, 'html'))
#         message = ('Subject here', 'Here is the message', EMAIL_HOST_USER, ['cl.jmunoz@gmail.com', 'juaa.munoz@duocuc.cl'])
#         # mailServer.sendmail(EMAIL_HOST_USER,
#         #                     destinatarios,
#         #                     mensaje.as_string())
#         mailServer.send_mass_mail((message), fail_silently=False)

#         # Cierre de la conexion
#         mailServer.close()

#     except Exception as e:
#         print(e)

def sendEmails(data):
    try:
        mailServer = smtplib.SMTP(EMAIL_HOST, EMAIL_PORT)
        print(mailServer.ehlo())
        mailServer.starttls()
        print(mailServer.ehlo())
        mailServer.login(EMAIL_HOST_USER,EMAIL_HOST_PASSWORD)

        # Construimos el mensaje simple
        mensaje = MIMEMultipart()
        mensaje['From'] =  "Sistema de Notificaciones AdminTask"

        # mensaje['To'] = data['email']

        mensaje['Subject'] = "Sistema de notificaciones de tareas"
        
        destinatarios = data['email']
        # destinatarios = ['juaa.munoz@duocuc.cl', 'cl.jmunoz@gmail.com']

        if data['evento'] == 'Tarea Rechazada':
            context = {
                'evento': data['evento'],
                'user': data['user'],
                'tarea': data['tarea'],
                'rechazadoPor': data['rechazadoPor'],
                'motivo': data['motivo']
            }

        elif data['evento'] == 'Actualizacion de tarea':
            context = {
                'evento': data['evento'],
                'user': data['user'],
                'tarea': data['tarea'],
            }

        elif data['evento'] == 'Finalización de tarea':
            context = {
                'evento': data['evento'],
                'tarea': data['tarea'],
                'motivo': 'Finalizada por sistema'
            }
            
        elif data['evento'] == 'Notificacion de Tarea':
            context = {
                'evento': data['evento'],
                'user': data['user'],
                'tarea': data['tarea'],
                'vence': data['vence'],
            }
        elif data['evento'] == 'Reporte Problema':
            context = {
                'evento': data['evento'],
                'user': data['user'],
                'tarea': data['tarea'],
                'problema': data['problema'],
            }
        

        content = render_to_string('email/email.html', context)

        mensaje.attach(MIMEText(content, 'html'))

        mailServer.sendmail(EMAIL_HOST_USER,
                            destinatarios,
                            mensaje.as_string())
        
    except Exception as e:
        print(e)

