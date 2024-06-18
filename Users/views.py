from django.shortcuts import render, redirect
from .forms import UserCreationFormWithEmail
from django.contrib.auth import authenticate, login as auth_login
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm

def register(request):
    if request.method == 'POST':
        form = UserCreationFormWithEmail(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login') 
    else:
        form = UserCreationFormWithEmail()
    return render(request, 'register.html', {'form': form})


