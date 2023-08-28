from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from .models import Task
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required,permission_required
from .forms import RegisterForm, NewTaskForm
from django.shortcuts import get_object_or_404



@login_required(login_url='/login')
def home(request):
    tasks = Task.objects.all().order_by('created_at')
    users = User.objects.all().order_by('date_joined')
    context = {'tasks':tasks,
               'users':users}
    return render(request,"main/home.html", context)

def sign_up(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('/home')
    else:
        form = RegisterForm()
        
    context = {"form":form}
    return render(request,'registration/login.html',context)

@login_required(login_url="/login")
def new_task(request,user_id):
    if request.method == "POST":
        form = NewTaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = get_object_or_404(User, id=user_id)
            task.save()

            return redirect("/home")

    else:
        form = NewTaskForm()
        
    context = {"form": form,
               "user_id":user_id}
    
    return render(request, 'main/task_form.html', context)

@login_required(login_url="/login")
def edit_task(request,edit_type,task_id):
    if request.method == "GET":
        if edit_type == "done":                
            task = get_object_or_404(Task, id=task_id)
            task.done = True
            task.save()
            
        elif edit_type == "notdone":
            task = get_object_or_404(Task, id=task_id)
            task.done = False
            task.save()
            
        elif edit_type == "edit":
            task = get_object_or_404(Task, id=task_id)
            form = NewTaskForm(instance=task)
            context={'form':form}
            return render(request,'main/task_form.html',context)
            
        else:
            task = get_object_or_404(Task, id=task_id)
            task.delete()
        
    else:
        task = get_object_or_404(Task, id=task_id)
        form = NewTaskForm(request.POST,instance=task)
        if form.is_valid():
            task = form.save()
            
    if request.user.is_staff or request.user.has_perm("todo_app.delete_task"):
        
        return redirect(request.META.get('HTTP_REFERER'))
    
    return redirect('/home')

@login_required(login_url='/login')
def user_profile(request,user_id):
    if request.method == "GET":
        user_i = get_object_or_404(User, id=user_id)
        tasks = Task.objects.all().order_by('created_at')
        
        context = {'user_i':user_i,
                   'tasks':tasks}
        return render(request,'main/user_profile.html',context)
    else:
        print("post")
        
    return redirect('/home')

@login_required(login_url="/login")
def remove_profile(request,user_id):
    if request.method == "GET":
        user = User.objects.filter(id=user_id).first()
        user.delete()
    
    return redirect("/home")