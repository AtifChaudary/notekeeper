from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from .models import *
from django.http import HttpResponse
import json
import os
import shutil
import datetime
import random

# Create your views here.
def login(request):
    if request.user.is_authenticated:
        return redirect("/dashboard/")
    if request.method == "POST":
        try:
            username = request.POST.get('username')
            password = request.POST.get('password')

            user_obj = User.objects.filter(username=username)
            
            if not user_obj.exists():
                messages.warning(request, 'User not found')
                return redirect("/")

            user_obj = authenticate(username=username, password=password)

            if user_obj:
                auth_login(request, user_obj)
                return redirect("/dashboard/")

            messages.warning(request, 'Wrong Credentials')
            return redirect("/")

        except Exception as e:
            messages.warning(request, 'Something went wrong!')
            return redirect("/")

    else:
        return render(request, 'login.html')
    
 
def register(request):
    if request.user.is_authenticated:
        return redirect("/dashboard/")
    if request.method == "POST":
        try:
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            username = request.POST.get('email')
            email = request.POST.get('email')
            password = request.POST.get('password')

            user_obj = User.objects.filter(username=username)

            if user_obj.exists():
                messages.warning(request, 'Email is Taken')
                return redirect("/register/")

            user_obj = User.objects.filter(email=email)

            if user_obj.exists():
                messages.warning(request, 'Email is Taken')
                return redirect("/register/")

            user_obj = User.objects.create(username=username, email=email, first_name=first_name, last_name=last_name)
            user_obj.set_password(password)
            user_obj.save()
                        
            messages.success(request, 'Your account has been created. Please login')
            return redirect("/")
        
        except Exception as e:
            messages.warning(request, 'Something went wrong!')
            return redirect("/register/")

    else:
        return render(request, 'register.html')   


@login_required(login_url='/')
def logout(request):
    auth_logout(request)
    return redirect("/")


@login_required(login_url='/')
def dashboard(request):
    notes = Note.objects.filter(user=request.user)
    context = {"notes": notes}
    return render(request, 'dashboard.html', context)
    
    
@login_required(login_url='/')
def notes(request, functionality):
    if functionality == 'add':
        title = request.POST.get('title')
        content = request.POST.get('content')
        note_obj = Note.objects.create(title=title, content=content, user=request.user)
        note_obj.save()
        
        messages.success(request, 'Note Added')
        return redirect('/dashboard/')
    elif functionality.startswith('edit'):
        note_id = int(functionality.split("-")[1])
        title = request.POST.get('edit_title')
        content = request.POST.get('edit_content')
        note_obj = Note.objects.get(id=note_id)
        note_obj.title = title
        note_obj.content = content
        note_obj.save()
        messages.success(request, 'Note Updated')
        return redirect('/dashboard/')
    elif functionality.startswith('delete'):
        note_id = int(functionality.split("-")[1])
        Note.objects.get(id=note_id).delete()
        messages.success(request, 'Note Deleted')
        return redirect('/dashboard/')