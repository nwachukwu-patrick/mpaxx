from django.http import HttpResponse
from django.shortcuts import redirect, render
from mpaxx import app


app = app.App()
def index(request):
        if request.session.get('username'):
                return redirect('dashboard')
        context = {
                'APP_NAME':app.APP_NAME,
                'DEVELOPER':app.DEVELEOPER
        }
        return render(request,'home.html',context=context)

def test(request):
        
        context = {
                'APP_NAME':app.APP_NAME,
                'DEVELOPER':app.DEVELEOPER
        }
        return render(request,'test.html',context=context)
def pricing(request):        
        context = {
                'APP_NAME':app.APP_NAME,
                'DEVELOPER':app.DEVELEOPER
        }
        return render(request,'pricing.html',context=context)

def help(request):        
        context = {
                'APP_NAME':app.APP_NAME,
                'DEVELOPER':app.DEVELEOPER
        }
        return render(request,'help.html',context=context)

def support(request):        
        context = {
                'APP_NAME':app.APP_NAME,
                'DEVELOPER':app.DEVELEOPER
        }
        return render(request,'support.html',context=context)