from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserSignUpForm, UserLogInForm
from django.contrib.auth import authenticate
from django.contrib.auth import login as Login
from django.contrib.auth import logout as Logout
from django.contrib.auth.models import User
from django.http import JsonResponse, HttpResponse, Http404
from django.contrib.sites.shortcuts import get_current_site  
from django.utils.encoding import force_bytes, force_text  
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode  
from django.template.loader import render_to_string
from .tokens import account_activation_token
from smtplib import SMTP_SSL
from email.mime.text import MIMEText

# Create your views here.
def signup(request):
    if request.method == 'POST':
        form = UserSignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.is_active = False
            user.save()
            current_url = get_current_site(request)
            mail_subject = 'Traders.am Email Confirmation'
            message = render_to_string(
                'users_app/sign_up_activation.html',
                {
                    'user': user,
                    'request': request,
                    'domain': current_url.domain,
                    'uid': urlsafe_base64_encode(force_bytes(user.id)),
                    'token': account_activation_token.make_token(user) 
                }
            )
            to_email= form.cleaned_data['email']
            with SMTP_SSL('smtp.yandex.ru', 465) as server:
                msg = MIMEText(message, 'html')
                msg['Subject'] = mail_subject
                msg['From'] = "Traders.am <noreply@traders.am>"
                
                server.login('noreply@traders.am', '2p%84=DUu#W4WT7*')
                server.sendmail(from_addr='noreply@traders.am', to_addrs=to_email, msg=msg.as_string())

            to_email = to_email[0] + '*' * len(to_email[1:to_email.index('@')-2]) + to_email[to_email.index('@')-2:] 
            return render(request, 'users_app/check_email.html', context={'email': to_email})
    else:
        form = UserSignUpForm()
    
    return render(request, 'users_app/sign_up.html', {'form': form})

def signup_activation(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(id=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if User and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, 'Your account has been confirmed. Now you are able to log in.')
    else:
        messages.error(request, 'Activation link is invalid!')
    return redirect('home')

def login(request):
    if request.method == 'POST':
        form = UserLogInForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            remember = form.cleaned_data.get('remember')
            user = authenticate(request, username=username, password=password)
            if user:
                Login(request, user)
                if not remember:
                    request.session.set_expiry(0)
                # else:
                #     request.session.set_expiry(60*60*24*2)
                return redirect('home')
            else:
                messages.error(request, 'Wrong Username/Email or Password')
    else:
        form = UserLogInForm()
    
    return render(request, 'users_app/log_in.html', {'form': form}) 

def logout(request):
    if request.user.is_authenticated:
        Logout(request)
        messages.success(request, f'Successfuly logged out.')
    return render(request, 'main_app/home.html')

def account(request):
    if not request.user.is_authenticated:
        return redirect('login')
    return render(request, 'users_app/account.html')

def ajax_account(request):
    dep = request.GET.get('dep')
    if dep == 'security':
        user = request.user
        email = user.email
        username = user.username
        return JsonResponse({'email': email, 'username': username})
    elif dep == 'watchlists':
        return JsonResponse({})
    elif dep == 'alerts':
        return JsonResponse({})
    elif dep == 'portfolio':
        return JsonResponse({})
    else:
        raise Http404(f'Department is not found {dep}')

        