from django.http import HttpResponse
from django.shortcuts import redirect, render
from authentication.models import User
from mpaxx import app
from django.contrib.auth import logout
from django.contrib.auth.hashers import make_password,check_password
from urllib.parse import parse_qs
from django.contrib.sessions.models import Session
from django.contrib.auth import authenticate

app = app.App()

def user_login(request):
        _user  = ''
        if request.session.get('username'):
                return redirect('dashboard')
        if request.POST:
                username_or_email = request.POST['email_username']
                password = request.POST['password']
                if not '@' in username_or_email:
                    try:                          
                        user_model =  User.objects.filter(username = username_or_email).get()
                        user_password = user_model.password
                        _user = user_model
                    except:
                        error_message = "Invalid username or email."
                        context = {
                        'APP_NAME':app.APP_NAME,
                        'DEVELOPER':app.DEVELEOPER,
                        'error_message': error_message
                        }
                        return render(request, 'login.html', context=context)
                
                elif  '@' in username_or_email:
                    try:                          
                        user_model =  User.objects.filter(email = username_or_email).get()
                        user_password = user_model.password
                        _user = user_model
                    except:
                        error_message = "Invalid username or email."
                        context = {
                        'APP_NAME':app.APP_NAME,
                        'DEVELOPER':app.DEVELEOPER,
                        'error_message': error_message
                        }
                        return render(request, 'login.html', context=context)
                
                else:
                    error_message = "Invalid username or email."
                    context = {
                    'APP_NAME':app.APP_NAME,
                    'DEVELOPER':app.DEVELEOPER,
                    'error_message': error_message
                    }
                    return render(request, 'login.html', context=context)
                if check_password(password,user_password):                     
                    request.session['role'] = _user.role
                    request.session['id'] = _user.id
                    request.session['username'] = _user.username
                    request.session['first_name'] = _user.first_name
                    request.session['last_name'] = _user.last_name
                    return redirect('dashboard')
                else:
                    error_message = "Invalid password"
                    context = {
                    'APP_NAME':app.APP_NAME,
                    'DEVELOPER':app.DEVELEOPER,
                    'error_message': error_message
                    }
                    return render(request, 'login.html', context=context)
                
        
                
    
        context = {
                    'APP_NAME':app.APP_NAME,
                    'DEVELOPER':app.DEVELEOPER
            }
        return render(request,'login.html',context=context)

    

def register(request):
    request.session.flush()
    if request.method == 'POST':
        first_name = request.POST['firstname']
        last_name = request.POST['lastname']
        username = request.POST['username']
        email = request.POST['email']
        phone = request.POST['phone']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        # Convert QueryDict to a regular dictionary
        data_dict = {key: request.POST.getlist(key)[0] if request.POST.getlist(key) else None for key in request.POST}

        if not first_name or not last_name or not  username or not  email or not  phone or not  password1 or not  password2:
            error = 'Check for empty Fields'
            context = {
                'APP_NAME':app.APP_NAME,
                'DEVELOPER':app.DEVELEOPER,
                'error_message':error
                }
            return render(request,'register.html',context=context)
        user_model = User()
        user_model.first_name = first_name
        user_model.last_name = last_name
        user_model.username = username
        user_model.phone = phone
        user_model.email = email
        user_model.password = make_password(password1)
        user_model.save()   
        user_model = User.objects.filter(username=username).get()
        if user_model.id == 1:
            user_model.role = 'admin'
            user_model.save()  
        # Set values from dictionary into session
        for key, value in data_dict.items():
            request.session[key] = value
        # request.session['password'] = password1
        request.session['role'] = User.objects.filter(username=username).get().role
        request.session['id'] = User.objects.filter(username=username).get().id
        return redirect('dashboard')
    context = {
                'APP_NAME':app.APP_NAME,
                'DEVELOPER':app.DEVELEOPER
        }
    return render(request,'register.html',context=context)

def user_logout(request):
    logout(request)
    return redirect('home')