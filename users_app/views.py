from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserSignUpForm, UserLogInForm
from django.contrib.auth import authenticate
from django.contrib.auth import login as Login
from django.contrib.auth import logout as Logout

# Create your views here.
def signup(request):
    if request.method == 'POST':
        form = UserSignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Accound has been created for {username}')
            return redirect('home')
    else:
        form = UserSignUpForm()
    
    return render(request, 'users_app/sign_up.html', {'form': form})

def login(request):
    if request.method == 'POST':
        form = UserLogInForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                Login(request, user)
                return redirect('home')
            else:
                messages.error(request, f'Wrong Username/Email or Password')
    else:
        form = UserLogInForm()
    
    return render(request, 'users_app/log_in.html', {'form': form}) 

def logout(request):
    if request.user.is_authenticated:
        Logout(request)
        messages.success(request, f'Successfuly logged out.')
    return render(request, 'main_app/home.html')

        