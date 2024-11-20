from django.shortcuts import render
from django.http import HttpResponse
from .models import Task
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect
from django.contrib import messages
from .forms import LoginForm, TaskForm
from django.contrib.auth.decorators import login_required
from django.db.models import Q
# Create your views here.

def loginPage(request):

    form = LoginForm()

    if request.method == 'POST':
        form = LoginForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request,user)
            return redirect('task')
        else:
            messages.error(request,'Invalid username or password')


    context={'form' : form}
    return render(request, 'login.html', context)
    


def logoutUser(request):
    logout(request)
    return redirect('login')



def registerPage(request):
    
    form = UserCreationForm()
    
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request,user)
            return redirect('task')
        else:
            messages.error(request,'An error occured during registration')

    context = {'form' : form}
    return render(request,'register.html',context)


@login_required
def task(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    form = TaskForm()

    if request.method == 'POST':
        title = request.POST.get('title')
        status = request.POST.get('status')
        priority = request.POST.get('priority')

        if title:
            Task.objects.create(title=title, status=status, priority=priority,user=request.user)
        else:
            messages.error(request,'you must enter a title')
        return redirect('task')

    if q:
        tasks = Task.objects.filter(
            Q(title__icontains=q) |
            Q(status__icontains=q) |
            Q(priority__icontains=q),
            user=request.user
        )
    else:
        tasks = Task.objects.filter(user=request.user)

        
    context = {'tasks': tasks, 'form': form, 'query' : q}
    return render(request, 'task_form.html', context)



@login_required
def updateTask(request, pk):
    task = Task.objects.get(id=pk,user=request.user)
    form = TaskForm(instance=task)

    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('task')


    context = {'form': form, 'task': task}
    return render(request, 'edit_task.html', context)



@login_required
def deleteTask(request, pk):
    try:
        task = Task.objects.get(id=pk,user=request.user)
    except Task.DoesNotExist:
        messages.error(request, "Task not found.")
        return redirect('task')

    if request.method == 'POST':
        task.delete()
        return redirect('task')

    return render(request, 'delete.html', {'task': task})