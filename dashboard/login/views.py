from django.shortcuts import render

def login(request):
    return render(request,'login/login.html')

def forgotPassword(request):
    return render(request,'login/forgot-password.html')

def lockscreen(request):
    return render(request,'login/lockscreen.html')

def recoverPassword(request):
    return render(request,'login/recover-password.html')