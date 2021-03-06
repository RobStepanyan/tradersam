from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserSignUpForm, UserLogInForm
from .models import Watchlist
from django.forms.models import model_to_dict
from django.core.exceptions import ValidationError, PermissionDenied
from django.core.validators import EmailValidator
from django.contrib.auth import authenticate, password_validation
from django.contrib.auth import login as Login
from django.contrib.auth import logout as Logout
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.http import JsonResponse, HttpResponse, Http404
from django.views.decorators.csrf import csrf_protect
from django.contrib.sites.shortcuts import get_current_site  
from django.utils.encoding import force_bytes, force_text  
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode  
from django.template.loader import render_to_string
from .tokens import account_activation_token
from smtplib import SMTP_SSL
from email.mime.text import MIMEText
from scraper_app.scraper_data import STATIC_OBJECTS
from scraper_app.models import AllAssetsLive, Countries, Types

# Create your views here.
def signup(request):
    if request.method == 'POST':
        form = UserSignUpForm(request.POST)
        if form.is_valid():
            if User.objects.filter(email=request.POST.get('email')).exists():
                messages.error(request, 'User with that email already exists.')
                return redirect('signup')

            if User.objects.filter(username__iexact=request.POST.get('username')).exists():
                messages.error(request, 'User with that username already exists.')
                return redirect('signup')

            user = form.save()
            user.is_active = False
            user.save()
            current_url = get_current_site(request)
            mail_subject = 'Traders.am Email Verification'
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

            to_email = to_email[:2] + '*' * len(to_email[2:to_email.index('@')-2]) + to_email[to_email.index('@')-2:] 
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
    if user and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, 'Your account has been confirmed. Now you are able to log in.')
    else:
        messages.error(request, 'Activation link is invalid!')
    return redirect('login')

def login(request):
    if request.user.is_authenticated:
        Logout(request)
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
                messages.error(request, 'Wrong Username or Password')
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
        user = request.user
        watchlists_raw = Watchlist.objects.filter(username=user.username).order_by('name')
        watchlists = []
        for watch in watchlists_raw:
            watch = model_to_dict(watch)
            name = watch['name']
            asset_links = []
            for asset in watch['asset_links']:
                for value in STATIC_OBJECTS.values():
                    static_model = None
                    if value['object'].objects.filter(link=asset).exists():
                        static_model = model_to_dict(value['object'].objects.get(link=asset))
                
                    if static_model:
                        if AllAssetsLive.objects.filter(link=asset).exists():
                            live_model = model_to_dict(AllAssetsLive.objects.get(link=asset))
                            live_model = {'last': live_model['last_price'],'change_perc': live_model['change_perc'], 'volume': live_model['volume']}
                        else:
                            live_model = {'last': 'N/A', 'change_perc': 'N/A', 'volume': 'N/A'}
                    else:
                        continue
                    
                    type_ = Types[Types.index(static_model['Type'])+1]
                    asset_dct = {
                        'type': static_model['Type'],
                        'country': static_model['country'],
                        'short_name': static_model['short_name'],
                        'last': live_model['last'],
                        'change_perc': live_model['change_perc'],
                        'volume': live_model['volume'],
                        'href': '/asset/' + static_model['country'].lower() + '/' + type_.lower() + '/' + str(static_model['id'])
                        }
                    asset_links.append(asset_dct)
            watchlists.append({'name': name, 'asset_links': asset_links})   

        return JsonResponse({'watchlists': watchlists})
    
    # elif dep == 'alerts':
    #     return JsonResponse({})
    # elif dep == 'portfolios':
    #     return JsonResponse({})
    else:
        raise Http404(f'Department is not found {dep}')

def ajax_change_username(request):
    new_username = request.GET.get('username')
    success_message = 'The username have been successfuly changed.'
    exists_message = 'A user with that username already exists.'
    
    if not request.user.is_authenticated:
        raise PermissionDenied('User is not authenticated')
    try:
        UnicodeUsernameValidator()(new_username)
    except ValidationError as e:
        # if new_username is not valid
        return JsonResponse({'valid':False, 'message': e.message})

    if request.user.email == new_username:
        return JsonResponse({'valid': False, 'message': 'The new username doesn\'t differ from the old one.'})

    # if new_username is valid
    user = request.user
    if User.objects.exclude(pk=user.pk).filter(username=new_username).exists():
        return JsonResponse({'valid':False, 'message': exists_message})
    else:
        user.username = new_username
        user.save()
        return JsonResponse({'valid': True, 'message': success_message})

def ajax_change_email(request):
    new_email = request.GET.get('email')

    if not request.user.is_authenticated:
        raise PermissionDenied('User is not authenticated')

    try:
        EmailValidator()(new_email)
    except ValidationError as e:
        # if new_email is not valid
        return JsonResponse({'valid': False, 'message': e.message})

    if request.user.email == new_email:
        return JsonResponse({'valid': False, 'message': 'The new email doesn\'t differ from the old one.'})

    user = request.user
    current_url = get_current_site(request)
    mail_subject = 'Traders.am Email Change Request'
    message = render_to_string(
        'users_app/email_reset.html',
        {
            'user': user,
            'request': request,
            'domain': current_url.domain,
            'uid': urlsafe_base64_encode(force_bytes(user.id)),
            'token': account_activation_token.make_token(user),
            'new_email': urlsafe_base64_encode(force_bytes(new_email)),
        }
    )
    to_email= user.email
    with SMTP_SSL('smtp.yandex.ru', 465) as server:
        msg = MIMEText(message, 'html')
        msg['Subject'] = mail_subject
        msg['From'] = "Traders.am <noreply@traders.am>"
        
        server.login('noreply@traders.am', '2p%84=DUu#W4WT7*')
        server.sendmail(from_addr='noreply@traders.am', to_addrs=to_email, msg=msg.as_string())
    
    return JsonResponse({'valid': True, 'message': f'Email verification link has been sent to {to_email}'})

def change_email(request, uidb64, token, new_email):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(id=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        return
   
    if user and account_activation_token.check_token(user, token):
        new_email = force_text(urlsafe_base64_decode(new_email))
        user.email = new_email
        user.save()
        messages.success(request, 'Your email has been changed.')
    else:
        messages.error(request, 'Email change link is invalid!')
    return redirect('home')

@csrf_protect
def ajax_change_password(request):
    if not request.user.is_authenticated:
        raise PermissionDenied('User is not authenticated')
            
    old = request.POST.get('old_pass')
    new1 = request.POST.get('new_pass1')
    new2 = request.POST.get('new_pass2')
    user = request.user

    if any([not old, not new1, not new2]):
        # if any value is empty
        return JsonResponse({'valid': False, 'message': 'Please fill up all the three fields.'})
    if not user.check_password(old):
        return JsonResponse({'valid': False, 'message': 'Old password is incorrect.'})
    if new1 != new2:
        return JsonResponse({'valid': False, 'message': 'The two password fields didn’t match.'})
    if old == new1 or old == new2:
        return JsonResponse({'vaild': False, 'message': 'The new password doesn\'t differ from the old one.'})
    else:
        try:
            password_validation.validate_password(new1, user)
        except ValidationError as e:
            errors = [str(error) for error in e]
            return JsonResponse({'valid': False, 'message': errors, 'iterable': True if len(errors) > 1 else None })
        
        user.set_password(new1)
        user.save()
        update_session_auth_hash(request, user)
        return JsonResponse({'valid': True, 'message': 'Password has been successfuly changed.'})

def password_reset(request):
    if request.method == 'POST':
        login = request.POST.get('login')
        if '@' in login:
            try:
                EmailValidator()(login)
            except ValidationError as e:
                return render(request, 'users_app/password_reset.html', {'valid': False, 'message': e})

            if not User.objects.filter(email=login).exists():
                e = ['A user with that email doesn\'t exists']
                return render(request, 'users_app/password_reset.html', {'valid': False, 'message': e})
            else:
                user = User.objects.get(email=login)
        
        else:
            try:
                UnicodeUsernameValidator()(login)
            except ValidationError as e:
                return render(request, 'users_app/password_reset.html', {'valid': False, 'message': e})

            if not User.objects.filter(username=login).exists():
                e = ['A user with that username doesn\'t exists']
                return render(request, 'users_app/password_reset.html', {'valid': False, 'message': e})
            else:
                user = User.objects.get(username=login)

        current_url = get_current_site(request)
        mail_subject = 'Traders.am Password Reset'
        message = render_to_string(
            'users_app/email_reset_pass.html',
            {
                'user': user,
                'request': request,
                'domain': current_url.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.id)),
                'token': account_activation_token.make_token(user),
            }
        )
        to_email= user.email
        with SMTP_SSL('smtp.yandex.ru', 465) as server:
            msg = MIMEText(message, 'html')
            msg['Subject'] = mail_subject
            msg['From'] = "Traders.am <noreply@traders.am>"
            
            server.login('noreply@traders.am', '2p%84=DUu#W4WT7*')
            server.sendmail(from_addr='noreply@traders.am', to_addrs=to_email, msg=msg.as_string())
        to_email = to_email[:2] + '*' * len(to_email[2:to_email.index('@')-2]) + to_email[to_email.index('@')-2:] 
        return render(request, 'users_app/check_reset_password.html', context={'email': to_email})
    # if request.method != 'POST'
    return render(request, 'users_app/password_reset.html')

def new_password(request, uidb64, token):
    if request.method == 'POST':
        new1 = request.POST.get('new_pass1')
        new2 = request.POST.get('new_pass2')
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(id=uid)
        if any([not new1, not new2]):
        # if any value is empty
            return render(
            request, 'users_app/new_password.html', {'valid': False, 'message': 'Please fill up all the fields.'})
        if new1 != new2:
            return render(
            request, 'users_app/new_password.html', {'valid': False, 'message': 'The two password fields didn’t match.'})
        try:
            password_validation.validate_password(new1, user)
        except ValidationError as e:
            errors = [str(error) for error in e]
            return render(
            request, 'users_app/new_password.html', {'valid': False, 'message': errors, 'iterable': True if len(errors) > 1 else None })
        
        user.set_password(new1)
        user.save()
        update_session_auth_hash(request, user)
        messages.success(request, 'Password has been successfuly changed.')
        return redirect('login')
    else:
        try:
            uid = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(id=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            messages.error(request, 'Activation link is invalid!')
            return redirect('home')

        if user and account_activation_token.check_token(user, token):
            return render(request, 'users_app/new_password.html')
        else:
            messages.error(request, 'Activation link is invalid!')
            return redirect('home')

def ajax_watchlist(request):
    user = User.objects.get(pk=request.user.pk)
    if request.GET['action'] == 'change_name':
        old_name = request.GET['old_name']
        new_name = request.GET['new_name']
        
        if Watchlist.objects.filter(username=user.username, name=new_name).exists():
            return JsonResponse({'error': True})
        
        obj = Watchlist.objects.get(username=user.username, name=old_name)
        obj.name = new_name
        obj.save()
    elif request.GET['action'] == 'delete':
        if Watchlist.objects.filter(username=user.username, name=request.GET['name']).exists():
            obj = Watchlist.objects.get(username=user.username, name=request.GET['name'])
            obj.delete()
    elif request.GET['action'] == 'create':
        Watchlist(
            name=request.GET['name'],
            username=user.username,
            asset_links=[]
        ).save()
    elif request.GET['action'] == 'edit':
        if Watchlist.objects.filter(username=user.username, name=request.GET['name']).exists():
            obj = Watchlist.objects.get(username=user.username, name=request.GET['name'])
            href = request.GET['href']
            # Extracting variables from href
            asset_end_index = href.index('asset/')+len('asset/')
            country = href[asset_end_index : asset_end_index+href[asset_end_index:].index('/')].upper() # us->US
            country_end_index = href.index(country.lower())+len(country)+1
            type_ = href[country_end_index : country_end_index+href[country_end_index:].index('/')].title() 
            if type_.lower() == 'etf':
                type_ = type_.lower()
            else:
                type_ = Types[Types.index(type_)-1] # Commodity -> cmdty
            id_ = int(href[-href[::-1].index('/'):])
        
            for key, value in STATIC_OBJECTS.items():
                if type_ in ['cmdty', 'crncy', 'crptcrncy']:
                    if type_ == value['type']:
                        link = value['object'].objects.get(id=id_).link
                        break
                else:
                    if country in key and type_ == value['type']:
                        link = value['object'].objects.get(id=id_).link
                        break

        if request.GET['sub_action'] == 'delete':
                obj.asset_links.remove(link)
                obj.save()
        
        elif request.GET['sub_action'] == 'add':
            obj.asset_links.append(link)
            obj.save()
            for value in STATIC_OBJECTS.values():
                static_model = None
                if value['object'].objects.filter(link=link).exists():
                    static_model = model_to_dict(value['object'].objects.get(link=link))
            
                if static_model:
                    if AllAssetsLive.objects.filter(link=link).exists():
                        live_model = model_to_dict(AllAssetsLive.objects.get(link=link))
                        live_model = {'change_perc': live_model['change_perc'], 'volume': live_model['volume']}
                    else:
                        live_model = {'change_perc': 'N/A', 'volume': 'N/A'}
                else:
                    continue
                
                type_ = Types[Types.index(static_model['Type'])+1]
                asset_dct = {
                    'type': static_model['Type'],
                    'country': static_model['country'],
                    'short_name': static_model['short_name'],
                    'change_perc': live_model['change_perc'],
                    'volume': live_model['volume'],
                    'href': '/asset/' + static_model['country'].lower() + '/' + type_.lower() + '/' + str(static_model['id'])
                    }
                return JsonResponse({'asset_dct': asset_dct})
    
    # elif request.GET['retrieve']:
    #     if Watchlist.objects.filter(username=user.username, name=request.GET['name']).exists():
    #         watch = model_to_dict(Watchlist.objects.get(username=user.username, name=request.GET['name']))
    #         name = watch['name']
    #         assets_list = []
    #         for asset in watch['asset_links']:
    #             for value in STATIC_OBJECTS.values():
    #                 static_model = None
    #                 if value['object'].objects.filter(link=asset).exists():
    #                     static_model = model_to_dict(value['object'].objects.get(link=asset))
                
    #                 if static_model:
    #                     if AllAssetsLive.objects.filter(link=asset).exists():
    #                         live_model = model_to_dict(AllAssetsLive.objects.get(link=asset))
    #                         if static_model.Type == 'crptcrcny':
    #                             live_model = {
    #                                 'last': live_model['last_price'], 'change_perc': live_model['change_perc'], 'volume': live_model['volume']}
    #                         else:
    #                             live_model = {
    #                                 'last': live_model['last_price'], 'change': live_model['change'], 'change_perc': live_model['change_perc'], 'volume': live_model['volume']}
    #                     else:
    #                         if static_model.Type == 'crptcrcny':
    #                             live_model = {
    #                                 'last': 'N/A', 'change_perc': 'N/A', 'volume': 'N/A'}
    #                         else:
    #                             live_model = {
    #                                 'last': 'N/A', 'change': 'N/A', 'change_perc': 'N/A', 'volume': 'N/A'}
    #                 else:
    #                     continue
                    
    #                 type_ = Types[Types.index(static_model['Type'])+1]
    #                 asset_dct = {
    #                     'type': static_model['Type'],
    #                     'country': static_model['country'],
    #                     'short_name': static_model['short_name'],
    #                     'live_model': live_model,
    #                     'href': '/asset/' + static_model['country'].lower() + '/' + type_.lower() + '/' + str(static_model['id'])
    #                     }
    #                 assets_list.append(asset_dct)
    #         return JsonResponse({'name': name, 'assets_list': assets_list})


    return JsonResponse({'error': False})
