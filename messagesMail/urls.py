from django.urls import path
from messagesMail import views

urlpatterns = [
    path('', views.sendEmails, name='sendEmails'), #Elemento de prueba para envio de correo

]