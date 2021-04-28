from django.shortcuts import render,redirect,Http404,HttpResponse
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from tasks.views import get_projects_from_slug, get_user_from_id
from projects.models import Project,Subscriber
from .models import Bug
from .forms import BugRegisterForm
from tasks.models import Task
from bs4 import BeautifulSoup

def removeHtml(string=""):
    string= BeautifulSoup(string,"lxml").text
    return string.replace('\n','<br>')

PATH = 'views/bugs/' 

def get_task_by_id(project,id):
    return Task.objects.filter(pk=id,project=project)

def get_bug_by_id(project,task,id):
    return Bug.objects.filter(pk=id,project=project,task=task)

def check_authorization(user,project):
   return Subscriber.objects.filter(project=project,subscriber=user).exists() or project.user_id == user

def initial_process(request,slug,task_id):
    user = request.user
    projects = get_projects_from_slug(slug)
    if not projects.exists():
        raise Http404()
    project = projects[0]
    tasks = get_task_by_id(project,task_id)
    if not tasks.exists():
        raise Http404()
    
    if not check_authorization(user,project):
        raise Http404()
    
    return project,tasks[0],user

def second_process(project,task,user,id):
    bugs = Bug.objects.filter(pk=id,project=project,task=task)
    if not bugs.exists():
        raise Http404()
    
    bug = bugs[0]

    if (bug.registered_by == user) or (project.user_id==user) or (task.assigned_to==user):
        return bug
    
    raise Http404()


@login_required
def create(request,slug,task_id):
    context = dict()
    project,task,user = initial_process(request,slug,task_id)
    if request.method == "POST":
        form = BugRegisterForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            description =  form.cleaned_data['description']
            reproduce = form.cleaned_data['reproduce']
            #reproduce = removeHtml(reproduce)
            bug = Bug(project=project,task=task,registered_by=user,name=name,description=description,reproduce=reproduce)
            bug.save()
            return redirect("task-details",slug=slug,id=task_id)
        else:
            context['errors'] = form.errors

    context['project'] = project
    context['task'] = task 
    return render(request,PATH+"create_bug.html",context=context)


@login_required
def delete(request,slug,task_id,id):
    context = dict()
    project,task,user = initial_process(request,slug,task_id)
    bug = second_process(project,task,user,id)
    if request.method == "POST":
        bug.delete()

    return redirect('task-details',slug=slug,id=task_id)


@login_required
def edit(request,slug,task_id,id):
    context = dict()
    project,task,user = initial_process(request,slug,task_id)
    bug = second_process(project,task,user,id)

    if request.method=="POST":
        form = BugRegisterForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            description =  form.cleaned_data['description']
            reproduce = form.cleaned_data['reproduce']
            #reproduce = removeHtml(reproduce)

            bug.name = name
            bug.description = description
            bug.reproduce = reproduce

            bug.save()
            return redirect('task-details',slug=slug,id=task_id)
        else:
            context['errors'] =form.errors
    
    context['project'] = project
    context['task'] = task
    context['bug'] = bug
    context['html_produced'] = removeHtml(bug.reproduce)
    return render(request,PATH+"bug_details.html",context=context)

@login_required
def toggle(request,slug,task_id,id):
    context = dict()
    project,task,user = initial_process(request,slug,task_id)
    bug = second_process(project,task,user,id)

    if request.method=="POST":
        bug.is_close = not bug.is_close
        bug.save()
    
    return redirect("task-details",slug=slug,id=task_id)


@login_required
def show(request,slug,task_id,id):
    context = dict()
    project,task,user = initial_process(request,slug,task_id)
    bug = get_bug_by_id(project,task,id)
    if not bug.exists():
        raise Http404()
    
    context['bug']=bug[0]
    context['project']=project
    context['task']=task
    context['html_produced'] = removeHtml(bug[0].reproduce)

    

    return render(request,PATH+"bug_details.html",context=context)
