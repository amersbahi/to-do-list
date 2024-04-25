# In views.py

from django.shortcuts import render, redirect
from django.urls import reverse
from .models import Task
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate, login, logout

from django.http import HttpResponseRedirect
from django.db import IntegrityError


def register(request):
     if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
     else:
        form = UserCreationForm()
     return render(request, 'toDo/html/register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('task-list')
    else:
        form = AuthenticationForm()
    return render(request, 'toDo/html/login.html', {'form': form})

def user_logout(request):
    logout(request)
    return redirect('login')
    

def task_list(request):
    tasks = Task.objects.all()
    return render(request, 'toDo/html/task_list.html', {'tasks': tasks})

def task_detail(request, task_id):
    task = Task.objects.get(id=task_id)
    return render(request, 'toDo/html/task_detail.html', {'task': task})

def task_create(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        Task.objects.create(title=title, description=description)
        return redirect('task-list')
    return render(request, 'toDo/html/task_create.html')

def task_update(request, task_id):
    task = Task.objects.get(id=task_id)
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        completed = request.POST.get('completed') == 'on'
        task.title = title
        task.description = description
        task.completed = completed
        task.save()
        return redirect('task-list')
    return render(request, 'toDo/html/task_update.html', {'task': task})

def task_delete(request, task_id):
    task = Task.objects.get(id=task_id)
    task.delete()
    return redirect('task-list')
