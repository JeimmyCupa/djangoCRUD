from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm 
from django.contrib.auth.models import User
from django.contrib.auth import login,logout,authenticate
from django.db import IntegrityError
from .forms import TaskForm
from .models import Task
from django.utils import timezone
from django.contrib.auth.decorators import login_required

# Create your views here.
def singup(request):
    if(request.method =="GET"):
        return render(request,'singup.html',
                  {'form':UserCreationForm})
    elif request.method == "POST":
        if request.POST["password1"] == request.POST["password2"]:
            #Crear usuario
            try:
                user = User.objects.create_user(username = request.POST["username"], password=request.POST["password1"])
                user.save()
                # Autentificación y creación de cookies
                login(request, user)
                return redirect('tasks')
            except IntegrityError:
                return render(request,'singup.html',{
                    'form':UserCreationForm,
                    'error':'El usuario ya se encuentra registrado.'
                })
        else:
            return render(request,'singup.html',{
                    'form':UserCreationForm,
                    'error':'Las contraseñas no coinciden..'
                })
@login_required
def singout(request):
    logout(request)
    return redirect('home')
  
  
def singin(request):
   if request.method == 'GET':
        return render(request,'singin.html',{
        'form':AuthenticationForm
         })
   elif request.method == 'POST':
        #Autenticar usuario
        user = authenticate(request, username = request.POST['username'],password=request.POST['password'])
        if user is None:
            return render(request,'singin.html',{
            'form':AuthenticationForm,
            'error':'Usuario o clave incorrecta'
            })
        else:
            #INICIAR SESIÓN EN EL NAVEGADOR
            login(request,user)
            return redirect('tasks') 
        
   
    
def home(request):
    return render(request, 'home.html')
@login_required
def tasks(request):
    #filter() recibe varios parametros para devolver valores datecompleted__isnull=True
    tasks = Task.objects.filter(user=request.user,datecompleted__isnull=True)
    return render(request, 'tasks.html',
                  {
                      'tasks' :tasks
                  })

@login_required
def task_completed(request):
    tasks = Task.objects.filter(user=request.user, datecompleted__isnull=False)
    return render(request,'tasks.html',{
        'tasks':tasks
    }
    )
@login_required
def create_task(request):
    if request.method == 'GET':
        return render(request, 'create_task.html',{
            'form':TaskForm
        })
    elif request.method == 'POST':
        try:
            #Usar el formulario creado para guardar el objeto en la base de datos
            form = TaskForm(request.POST)
            task = form.save(commit=False) #Nueva tarea devuelta a partir de los datos del form creado.
            task.user = request.user # Necesita añadir el usuario que creo la tarea
            task.save()
            return redirect('tasks')
        except ValueError:
            return render(request, 'create_task.html',{
            'form':TaskForm,
            'error':'Ingresa datos validos'
        })
@login_required           
def task_detail(request,task_id):
    if request.method == 'GET':
        # task = Task.objects.get(id = task_id)
        task = get_object_or_404(Task,pk = task_id,user=request.user)
        form = TaskForm(instance=task)
        return render(request, 'task_detail.html',{'task':task, 'form':form})
    elif request.method == 'POST':
        #Actualizar datos del objeto en la base de datos
        try:
            task = get_object_or_404(Task,pk = task_id,user=request.user)
            form = TaskForm(request.POST,instance=task)
            form.save()
            return redirect('tasks')
        except ValueError:
           return render(request, 'task_detail.html',{'task':task, 'form':form,'error':'Error en la actualizacion'})
@login_required      
def complete_task(request, task_id):
    task =  get_object_or_404(Task,pk=task_id, user=request.user)
    if request.method == 'POST':
        task.datecompleted = timezone.now()
        task.save()
        return redirect('tasks')
@login_required
def delete_task(request, task_id):
     task =  get_object_or_404(Task,pk=task_id, user=request.user)
     if request.method == 'POST':
         task.delete()
         return redirect('tasks')
        