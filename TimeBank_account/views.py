from django.shortcuts import render, redirect

from django.contrib.auth.models import User
from django.contrib import auth

# Create your views here.
def register(request):
    if request.method == 'POST':
        user = User.objects.create_user(username=request.POST['username'], password=request.POST['password'])
        auth.login(request, user)
        return redirect('index')
    return render(request, 'register.html')

def login(request):
    return render(request, 'login.html')

def logout(request):
    pass