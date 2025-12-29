from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.utils import timezone

from .models import Task
from .forms import TaskForm


# ================= HOME / TASK LIST =================
@login_required
def home(request):
    today = timezone.now().date()

    if request.method == "POST":
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.save()
            return redirect('home')
    else:
        form = TaskForm()

    tasks = Task.objects.filter(user=request.user, completed=False)

    context = {
        'form': form,
        'today_tasks': tasks.filter(due_date=today),
        'pending_tasks': tasks.filter(due_date__gt=today),
        'overdue_tasks': tasks.filter(due_date__lt=today),
    }
    return render(request, "index.html", context)


# ================= REGISTER =================
def register_view(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()

    return render(request, "register.html", {'form': form})


# ================= LOGIN =================
def login_view(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('home')

    return render(request, "login.html")


# ================= LOGOUT =================
def logout_view(request):
    logout(request)
    return redirect('login')
