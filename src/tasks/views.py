from django.shortcuts import render,redirect,Http404,HttpResponse
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from users.models import Users
from projects.models import Project,Subscriber
from .models import Task
from .forms import TaskCreationForm

def get_projects_from_slug(slug=None):
    
    return Project.objects.filter(slug=slug)
   
def get_user_from_id(id):
    return Users.objects.get(pk=id)

def return_alert_message(message=""):
    return HttpResponse(f"<script>alert('{message}');location.reload('/users/')</script>")

@login_required
def create_task(request,slug):
    user = request.user
    context = dict()
    context['slug']=slug
    projects = get_projects_from_slug(slug=slug).filter(Q(user_id=request.user)|Q(subscriber__subscriber=request.user))
    if not projects.exists() :
        raise Http404()
    project = projects[0]
    context['subscribers']=project.subscriber_set.all()
    if request.method=="POST":
        taskForm = TaskCreationForm(request.POST)
        if taskForm.is_valid():
            assigned_to_id = taskForm.cleaned_data['assigned_to']
            name = taskForm.cleaned_data['name']
            description = taskForm.cleaned_data['description']
            resources = taskForm.cleaned_data['resources']

            try:
                assigned_to = get_user_from_id(assigned_to_id)

                new_task = Task(project=project,assigned_to=assigned_to,name=name,description=description,resources=resources)
                new_task.save()
                return redirect('project_details',slug=slug)
            except Users.DoesNotExist:
                context['errors']="No Such User exists"
                pass
            except Subscriber.DoesNotExist:
                context['errors'] = "The User isn't Subscribed to the project"
                pass
        
    return render(request,'views/tasks/create_task.html',context=context)
    
@login_required
def toggle_is_done(request,slug,id):
    user = request.user
    projects = get_projects_from_slug(slug).filter(task__id=id).filter(Q(subscriber__subscriber=user)|Q(user_id=user))
    if not projects.exists():
        raise Http404()
    
    try:
        project = projects[0]
        task = Task.objects.get(id = id,project=project)
        task.is_done = not task.is_done
        task.save()
    except Task.DoesNotExist:
        return return_alert_message("Task Doesn't Exists")
    
    return redirect('project_details',slug=slug)


@login_required
def delete_task(request,slug,id):
    user = request.user
    projects = get_projects_from_slug(slug).filter(user_id=request.user)
    if not projects.exists():
        raise Http404()
    
    if request.method == "POST":
        try:
            task=Task.objects.get(project=projects[0],id=id)
            task.delete()
        except Task.DoesNotExist:
            return return_alert_message("The task doesn't exists")
    
    return redirect('project_details',slug=slug)



@login_required
def edit_task(request,slug,id):
    user = request.user
    context = dict()
    context['slug']=slug
    projects = get_projects_from_slug(slug).filter(Q(subscriber__subscriber=user)|Q(user_id=user))
    if not projects.exists():
        raise Http404()
    
    try:
        task=Task.objects.get(project=projects[0],id=id)
        
        if request.method == "POST":
            taskForm = TaskCreationForm(request.POST)
            if taskForm.is_valid():
                task.name = taskForm.cleaned_data['name']
                task.description = taskForm.cleaned_data['description']
                task.resources = taskForm.cleaned_data['resources']
                task.deadline=taskForm.cleaned_data['deadline']
                task.save()
                return redirect('project_details',slug=slug)
            else:
                context['errors']=taskForm.errors
    except Task.DoesNotExist:
        raise Http404()
    
    print(task)
    context['task']=task
    context['subscribers']=projects[0].subscriber_set.all()
    return render(request,"views/tasks/edit_task.html",context=context)
    
    

    
@login_required
def task_details(request,slug,id):
    user = request.user
    context = dict()
    context['slug']=slug
    projects = get_projects_from_slug(slug).filter(Q(subscriber__subscriber=user)|Q(user_id=user))
    if not projects.exists():
        raise Http404()
    
    try:
        task=Task.objects.get(project=projects[0],id=id)
        
    except Task.DoesNotExist:
        raise Http404()
    
    context['task']=task
    context['open_bugs'] = task.bug_set.filter(is_close=False)
    context['closed_bugs'] = task.bug_set.filter(is_close=True)
    
    return render(request,"views/tasks/task_details.html",context=context)


    
    



