from django.urls import path
from messagesMail import views

urlpatterns = [
    path('', views.testmail, name='testmail'), #Elemento de prueba para envio de correo

]