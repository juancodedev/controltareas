from django.shortcuts import redirect, render
from controltareas.settings import EMAIL_HOST, EMAIL_PORT, EMAIL_HOST_USER, EMAIL_HOST_PASSWORD
import smtplib, ssl
from django.http.request import HttpRequest

# Create your views here.
def sendEmails(request):#email,message
    
    receiver = 'cl.jmunoz@gmail.com'
    # messages = """\
    # Subject: Esta es una Prueba de correo.
    
    # Este mensaje fue enviado desde control de tareas django."""
    messages = """\
Subject: Esta es una prueba de correo

This message is sent from Python."""

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(EMAIL_HOST, EMAIL_PORT, context=context) as server:
        server.login(EMAIL_HOST_USER, EMAIL_HOST_PASSWORD)
        server.sendmail(EMAIL_HOST,receiver,messages)
        
        
    return redirect('login')
        
    # return None