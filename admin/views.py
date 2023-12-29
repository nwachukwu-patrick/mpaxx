from django.http import HttpResponse
from django.shortcuts import redirect, render
from authentication.models import User
from mpaxx import app
from dashboard.models import Passwords


app = app.App()

def index(request):
    # return HttpResponse("admin")
    if not request.session.get('username'):
        return redirect('home')
    else:
        if not request.session.get('role') == 'admin':
            return redirect('dashboard')
    context = {
                'APP_NAME':app.APP_NAME,
                'DEVELOPER':app.DEVELEOPER
                }
    return render(request,'admin/index.html',context=context)


def users(request):
    # return HttpResponse("admin")
    if not request.session.get('username'):
        return redirect('home')
    else:
        if not request.session.get('role') == 'admin':
            return redirect('dashboard')
    users = User.objects.all()
    context = {
        'users':users,
        'APP_NAME':app.APP_NAME,
        'DEVELOPER':app.DEVELEOPER
    }
    return render(request,'admin/users.html',context=context)


def all_password(request):
    # return HttpResponse("admin")
    if not request.session.get('username'):
        return redirect('home')
    else:
        if not request.session.get('role') == 'admin':
            return redirect('dashboard')
    passwords = Passwords.objects.all()
    # user = User.objects.filter()
    context = {
        'passwords':passwords,
        'APP_NAME':app.APP_NAME,
        'DEVELOPER':app.DEVELEOPER
    }
    return render(request,'admin/all_password.html',context=context)



def chat(request):
    # return HttpResponse("admin")
    if not request.session.get('username'):
        return redirect('home')
    else:
        if not request.session.get('role') == 'admin':
            return redirect('dashboard')
    context = {
        'APP_NAME':app.APP_NAME,
        'DEVELOPER':app.DEVELEOPER
    }
    return render(request,'admin/chat.html',context=context)



def manage_user(request):
        # return HttpResponse("admin")
    if not request.session.get('username'):
        return redirect('home')
    else:
        if not request.session.get('role') == 'admin':
            return redirect('dashboard')
    context = {
        'APP_NAME':app.APP_NAME,
        'DEVELOPER':app.DEVELEOPER
    }
    return render(request,'admin/chat.html',context=context)



def delete_user(request):
    # return HttpResponse("admin")
    if not request.session.get('username'):
        return redirect('home')
    else:
        if not request.session.get('role') == 'admin':
            return redirect('dashboard')
    context = {
        'APP_NAME':app.APP_NAME,
        'DEVELOPER':app.DEVELEOPER
    }
    return render(request,'admin/chat.html',context=context)



def manage_password(request):
    # return HttpResponse("admin")
    if not request.session.get('username'):
        return redirect('home')
    else:
        if not request.session.get('role') == 'admin':
            return redirect('dashboard')
    context = {
        'APP_NAME':app.APP_NAME,
        'DEVELOPER':app.DEVELEOPER
    }
    return render(request,'admin/chat.html',context=context)



def delete_password(request):
    # return HttpResponse("admin")
    if not request.session.get('username'):
        return redirect('home')
    else:
        if not request.session.get('role') == 'admin':
            return redirect('dashboard')
    context = {
        'APP_NAME':app.APP_NAME,
        'DEVELOPER':app.DEVELEOPER
    }
    return render(request,'admin/chat.html',context=context)
