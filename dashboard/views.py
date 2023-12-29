import csv
from io import BytesIO, TextIOWrapper
import json
import os
import secrets
import string
from django.http import HttpResponse, StreamingHttpResponse
from django.shortcuts import redirect, render
from mpaxx import app
from .models import Passwords as password_model
from django.template.loader import render_to_string
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.platypus import Table, TableStyle
from django.contrib.auth import authenticate
from authentication.models import User

# Create your views here.

app = app.App()

def index(request):
    if not request.session.get('username'):
        return redirect('home')
    else:
        if request.session['role'] == 'admin':
            return redirect('admin')
    user_data = {
        'username': request.session.get('username'),
        # Add more user-related data if needed
    }
    context = {
                'APP_NAME':app.APP_NAME,
                'DEVELOPER':app.DEVELEOPER,
                'user_data': user_data
                }
    return render(request, 'user/index.html', context=context)


def generate_password(request):     
     if not request.session.get('username'):
        return redirect('home')
     if request.method == 'POST':
        if request.POST.get('save_password'):
            name = request.POST.get('name')
            app_name = request.POST.get('app_name')
            generated_password = request.POST.get('generated_password')
            password_length = request.POST.get('length')
            if  not generated_password or not name or not app_name:
                error = 'Please Generate Password and Fill the neccesary details Before this operation'
                
                context = {
                    'APP_NAME':app.APP_NAME,
                        'DEVELOPER':app.DEVELEOPER,
                        'user_data': request.session.get('username'),
                        'length':password_length,
                        'error':error
                }
                return render(request, 'user/generatepassword.html', context=context)

            # Create or update an instance of your password model
            password_entry = password_model()
            
            # Update fields
            password_entry.name = name
            password_entry.app_name = app_name
            password_entry.generated_password = generated_password
            password_entry.password_length = password_length
            password_entry.user_id = request.session.get('id')
            
            password_entry.save()  # Save changes to the database


            context = {
                'APP_NAME':app.APP_NAME,
                    'DEVELOPER':app.DEVELEOPER,
                    'user_data': request.session.get('username'),
                    'length':password_length
            }
            return render(request, 'user/generatepassword.html', context=context)
        else:
            length = int(request.POST.get('length', 12))  # Get the desired length from the form (default: 12)
            characters = string.ascii_letters + string.digits + string.punctuation  # Include letters, digits, and symbols
            generated_password = ''.join(secrets.choice(characters) for _ in range(length))
            context = {
                'APP_NAME':app.APP_NAME,
                    'DEVELOPER':app.DEVELEOPER,
                    'user_data': request.session.get('username'),
                    'generated_password': generated_password,
                    'length':length
            }
            return render(request, 'user/generatepassword.html', context=context)
     context = {
                    'APP_NAME':app.APP_NAME,
                    'DEVELOPER':app.DEVELEOPER, 
                    'user_data': request.session.get('username'),
                    'length':12
                    }
     return render(request,'user/generatepassword.html',context)



def view_password(request):
    if not request.session.get('username'):
        return redirect('home')
    passwords = password_model.objects.filter(user_id=request.session.get('id'))
    context = {
                    'APP_NAME':app.APP_NAME,
                    'DEVELOPER':app.DEVELEOPER,
                    'data': passwords
                    }
    return render(request,'user/view-password.html',context=context)


def update_password(request):
    if not request.session.get('username'):
        return redirect('home')
    if request.POST.get('generate'):
        length = int(request.POST.get('length', 12))  # Get the desired length from the form (default: 12)
        characters = string.ascii_letters + string.digits + string.punctuation  # Include letters, digits, and symbols
        generated_password = ''.join(secrets.choice(characters) for _ in range(length))
        passwords = password_model.objects.filter(id = request.GET.get('edit'))
        context = {
                    'APP_NAME':app.APP_NAME,
                    'DEVELOPER':app.DEVELEOPER,                    
                    'data': passwords,
                    'generated_password':generated_password,
                    'length':length
                    }
        return render(request,'user/edit_password.html',context=context)
    if request.POST.get('update'):
        name = request.POST.get("name")
        app_name = request.POST.get("app_name")
        generated_password = request.POST.get("password")
        length = request.POST.get("length")
        pass_id = request.POST.get('id')
        password_table  = password_model.objects.filter(id=pass_id).get()
        password_table.name = name
        password_table.app_name = app_name
        password_table.password_length = length
        password_table.generated_password = generated_password
        password_table.save()
        passwords = password_model.objects.filter(id = pass_id)
        context = {
                    'APP_NAME':app.APP_NAME,
                    'DEVELOPER':app.DEVELEOPER,                    
                    'data': passwords
                    }
        return render(request,'user/edit_password.html',context=context)

    if request.GET.get('edit'):        
        passwords = password_model.objects.filter(id = request.GET.get('edit'))
        context = {
                    'APP_NAME':app.APP_NAME,
                    'DEVELOPER':app.DEVELEOPER,                    
                    'data': passwords
                    }
        return render(request,'user/edit_password.html',context=context)
    passwords = password_model.objects.filter(user_id=request.session.get('id'))
    context = {
                    'APP_NAME':app.APP_NAME,
                    'DEVELOPER':app.DEVELEOPER,
                    'data': passwords
                    }
    return render(request,'user/update-password.html',context=context)

def delete_password(request):
    if not request.session.get('username'):
        return redirect('home')
    passwords = password_model.objects.filter(id=request.GET.get('id'))
    if request.GET.get('response'):
        password_table = password_model.objects.filter(id=request.GET.get('id'))
        password_table.delete()
        return redirect('view password')
    context = {
                    'APP_NAME':app.APP_NAME,
                    'DEVELOPER':app.DEVELEOPER,
                    'data': passwords
                    }
    return render(request,'user/delete_password.html',context=context)


def import_password(request):
    if not request.session.get('username'):
        return redirect('home')
    if request.method == 'POST' and request.FILES.get('file'):
        uploaded_file = request.FILES['file']
        # Process the uploaded file to extract password data based on its format
        # Example: If the uploaded file is CSV
        if uploaded_file.name.endswith('.csv'):
             # Ensure the file is read in text mode
            csv_file = TextIOWrapper(uploaded_file.file, encoding='utf-8')
            passwords_data = csv.reader(csv_file)
            for row in passwords_data:
                try:
                    password_length = int(row[3])
                except (ValueError, IndexError):
                    password_length = 0  # Default value if conversion fails or data is missing
                if not password_length <= 0:
                    password_model.objects.create(
                        user_id = request.session.get('id'),
                        name=row[0],
                        app_name=row[1],
                        generated_password=row[2],
                        password_length=password_length
                    )
            context = {
                    'APP_NAME':app.APP_NAME,
                    'DEVELOPER':app.DEVELEOPER,
                    'success_message': 'Passwords imported successfully'
                    }
            return render(request, 'user/import_password.html', context=context)
        elif uploaded_file.name.endswith('.json'):
            try:
                # Decode the JSON file
                passwords_data = json.load(uploaded_file)
                
                for item in passwords_data:
                    # Assuming the JSON structure has 'name', 'app_name', 'generated_password', 'password_length'
                    password_length = int(item.get('Password Length', 0))
                    if password_length > 0:
                        password_model.objects.create(
                            user_id=request.session.get('id'),
                            name=item.get('Name', ''),
                            app_name=item.get('App Name', ''),
                            generated_password=item.get('Generated Password', ''),
                            password_length=password_length
                        )
                context = {
                    'APP_NAME':app.APP_NAME,
                    'DEVELOPER':app.DEVELEOPER,
                    'success_message': 'Passwords imported successfully'
                    }
                return render(request, 'user/import_password.html',context=context)
            except json.JSONDecodeError:
                pass  # Handle JSON decoding errors here
        elif uploaded_file.name.endswith('.txt'):
            try:
                passwords_data = uploaded_file.read().decode('utf-8')
                entries = passwords_data.split('\n\n')  # Entries separated by double newlines
                
                for entry in entries:
                    lines = entry.strip().split('\n')  # Split entry into lines
                    password_data = {}
                    for line in lines:
                        parts = line.split(': ', 1)  # Split key-value pairs
                        if len(parts) == 2:  # Ensure it's a valid key-value pair
                            key, value = parts
                            password_data[key] = value
                    
                    # Extract data and create model instance
                    try:
                        password_length = int(password_data.get('Password Length', '0'))
                        if password_length > 0:
                            password_model.objects.create(
                                user_id=request.session.get('id'),
                                name=password_data.get('Name', ''),
                                app_name=password_data.get('App Name', ''),
                                generated_password=password_data.get('Generated Password', ''),
                                password_length=password_length
                            )
                    except ValueError:
                        pass  # Handle conversion errors
                context = {
                    'APP_NAME':app.APP_NAME,
                    'DEVELOPER':app.DEVELEOPER,
                    'success_message': 'Passwords imported successfully'
                    }
                            
                return render(request, 'user/import_password.html', context=context)
            except UnicodeDecodeError:
                pass  # Handle Unicode decoding errors here
            
    context = {
                    'APP_NAME':app.APP_NAME,
                    'DEVELOPER':app.DEVELEOPER
                    }
    return render(request, 'user/import_password.html',context=context)


def export_password(request, file_format = ''):
    if not request.session.get('username'):
        return redirect('home')
    if file_format:
        if file_format == 'csv':
            passwords = password_model.objects.filter(user_id=request.session.get('id')) # Retrieve all password data
            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename="passwords.csv"'
            # Write password data to CSV file
            csv_writer = csv.writer(response)
            csv_writer.writerow(['Name', 'App Name', 'Generated Password', 'Password Length'])

            for password in passwords:
                csv_writer.writerow([password.name, password.app_name, password.generated_password, password.password_length])

            return response
        elif file_format == 'txt':
            passwords = password_model.objects.filter(user_id=request.session.get('id'))  # Retrieve all password data
            response = HttpResponse(content_type='text/plain')
            response['Content-Disposition'] = 'attachment; filename="passwords.txt"'

            # Write password data to TXT file
            for password in passwords:
                response.write(f"Name: {password.name}\n")
                response.write(f"App Name: {password.app_name}\n")
                response.write(f"Generated Password: {password.generated_password}\n")
                response.write(f"Password Length: {password.password_length}\n\n")

            return response
        elif file_format == 'json':
            passwords = password_model.objects.filter(user_id=request.session.get('id')) # Retrieve all password data

            password_list = []
            for password in passwords:
                password_data = {
                    'Name': password.name,
                    'App Name': password.app_name,
                    'Generated Password': password.generated_password,
                    'Password Length': password.password_length
                }
                password_list.append(password_data)

            # Create JSON response
            response = HttpResponse(json.dumps(password_list), content_type='application/json')
            response['Content-Disposition'] = 'attachment; filename="passwords.json"'
            return response
        elif file_format == 'html':
            passwords = password_model.objects.filter(user_id=request.session.get('id'))  # Retrieve all password data
            context = {'passwords': passwords}

            # Render the password data into an HTML table
            rendered_table = render_to_string('passwords_table.html', context)

            # Create HTML response
            response = HttpResponse(rendered_table, content_type='text/html')
            response['Content-Disposition'] = 'attachment; filename="passwords.html"'
            return response
        elif file_format == 'pdf':
            passwords =  password_model.objects.filter(user_id=request.session.get('id'))  # Retrieve all password data
            
        # Create a PDF document using ReportLab
            response = HttpResponse(content_type='application/pdf')
            response['Content-Disposition'] = 'attachment; filename="passwords.pdf"'

            buffer = BytesIO()
            pdf = canvas.Canvas(buffer, pagesize=letter)

            data = [
                ['Name', 'App Name', 'Generated Password', 'Password Length']
            ]
            for password in passwords:
                data.append([password.name, password.app_name, password.generated_password, password.password_length])

            # Create a PDF table
            table = Table(data)
            style = TableStyle([('BACKGROUND', (0, 0), (-1, 0), '#77DD77'),
                                ('TEXTCOLOR', (0, 0), (-1, 0), (0, 0, 0)),
                                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold')])
            table.setStyle(style)
            width, height = letter
            margin_top = 100  # Adjust this value for your desired top margin

            table.wrapOn(pdf, width, height)
            table.drawOn(pdf, 30, height - margin_top)

            pdf.save()
            pdf_data = buffer.getvalue()
            buffer.close()

            response.write(pdf_data)

            return response

        else:
            context = {
                        'APP_NAME':app.APP_NAME,
                        'DEVELOPER':app.DEVELEOPER,
                        'error':"Unsupported file format"
                        }
            return render(request,'user/export_password.html',context=context)
            # Implement similar export logic for other file formats (JSON, TXT, etc.)
    context = {
                    'APP_NAME':app.APP_NAME,
                    'DEVELOPER':app.DEVELEOPER
                    }
    return render(request,'user/export_password.html',context=context)


def account(request):
    user = User.objects.filter(id=request.session.get('id')).get()
    if request.POST:
        username = request.POST['username']
        first_name  = request.POST['first_name']
        last_name  = request.POST['last_name']
        age = request.POST['age']
        phone = request.POST['phone']
        user.username = username
        user.first_name = first_name
        user.last_name = last_name
        user.age = age
        user.phone = phone
        user.save()
    context = {
                    'APP_NAME':app.APP_NAME,
                    'DEVELOPER':app.DEVELEOPER,
                    'user':user
                    }
    return render(request,'user/account.html',context=context)

def checkout(request):        
        context = {
                'APP_NAME':app.APP_NAME,
                'DEVELOPER':app.DEVELEOPER
        }
        return render(request,'user/checkout.html',context=context)


def payment(request):        
        context = {
                'APP_NAME':app.APP_NAME,
                'DEVELOPER':app.DEVELEOPER
        }
        return render(request,'user/payment.html',context=context)

def notification(request):        
        context = {
                'APP_NAME':app.APP_NAME,
                'DEVELOPER':app.DEVELEOPER
        }
        return render(request,'user/notification.html',context=context)






