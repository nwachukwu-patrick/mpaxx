"""
URL configuration for mpaxx project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static
from authentication import views as auth
from dashboard import views as dashboard
from home import views as home
from admin import views as admin
from django.views.generic import TemplateView



urlpatterns = [
    path('admin/', admin.index,name="admin"),
    path('',include('home.urls'),name='home'),
    path('login/',auth.user_login,name="login"),
    path('register/',auth.register,name="register"),
    path('logout/',auth.user_logout,name="logout"),
    path('dashboard/',dashboard.index, name = 'dashboard'),
    path('generate-password/',dashboard.generate_password,name='generate password'),
    path('view-password/',dashboard.view_password,name="view password"),
    path('update-password/',dashboard.update_password, name="update password"),
    path('delete-password/',dashboard.delete_password,name="Delete password"),
    path('import-password/',dashboard.import_password,name="import password"),
    path('export-password/<str:file_format>/', dashboard.export_password, name='export password'),
    path('export-password/', dashboard.export_password, name='export password'),
    path('pricing/',home.pricing, name='pricing'),
    path('payment/',dashboard.payment, name='payment'),
    path('help/',home.help, name='help'),
    path('checkout/',dashboard.checkout, name='checkout'),
    path('account/',dashboard.account, name='account'),
    path('notification/',dashboard.notification, name='notification'),
    path('support/',home.support, name='support'),
    path('users/',admin.users, name='users'),
    path('all_password/',admin.all_password,name="all password"),
    path('chat/',admin.chat, name="chat"),
    path('manage_user/',admin.manage_user, name="manage user"),
    path('delete_user/',admin.delete_user, name="delete user"),
    path('manage_password/',admin.manage_password, name="manage password"),
    path('delete_password/',admin.delete_password, name="delete password"),
] 