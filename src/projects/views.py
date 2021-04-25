from django.shortcuts import render,redirect,HttpResponse
from django.http import Http404
from django.db.models import Q
from .models import Project,Subscriber
from django.contrib.auth.decorators import login_required
from .forms import ProjectForm,ProjectEditForm,ProjectJoinForm
from users.models import Users

def all_projects(request):
    projects=Project.objects.filter(Q(user_id=request.user.id)|Q(subscriber__subscriber=request.user)).order_by('-created_at')
    return projects


@login_required
def create_project(request):
    content= dict()
    if request.method == "POST":
        projectFm = ProjectForm(request.POST)
        if projectFm.is_valid():
            project_name = projectFm.cleaned_data.get('project_name',None)            
            description = projectFm.cleaned_data.get('description',None)            
            budget = projectFm.cleaned_data.get('budget',None)
            user = request.user
            print(Project.objects.filter(slug=unique_slugify(project_name)))
            try:
                project = Project(project_name=project_name,user_id=user,description=description,budget=budget)
                project.save()
                

            except Exception as e:
                print(e)       
        else:
            content['errors']=projectFm.errors

        return redirect('user_home',**content)


@login_required 
def edit_project(request,slug):
    proj = Project.objects.filter(user_id=request.user.id,slug=slug)
    context = dict()
    if proj.exists():
        project = proj[0]
        if request.method=="POST":
            updateForm = ProjectEditForm(request.POST)
            if updateForm.is_valid():
                project.project_name = updateForm.cleaned_data['project_name']
                project.description = updateForm.cleaned_data['description']
                project.budget = updateForm.cleaned_data['budget']
                project.isClosed = updateForm.cleaned_data['isClosed']
                project.save()
                return redirect('user_home')
            else:
                context['errors']=updateForm.errors
        context['project'] = project
        return render(request,'views/projects/edit_project.html',context=context)

        pass
    else:
        raise Http404("Project not found")
    pass

@login_required
def delete_project(request,slug):
    proj = Project.objects.filter(user_id=request.user.id,slug=slug)
    if proj.exists():
        proj.delete()
        return redirect('user_home')
        pass
    else:
        raise Http404("Project not found")


@login_required
def join_project(request):
    joinForm = ProjectJoinForm(request.GET)
    if joinForm.is_valid():
            slug = joinForm.cleaned_data['slug']
            proj = Project.objects.filter(slug=slug).exclude(Q(user_id=request.user)|Q(subscriber__subscriber=request.user))
            if proj.exists():
                
                project=proj[0]
                user = request.user
                subscriber = Subscriber(project=project,subscriber=user)
                subscriber.save()
                return redirect('user_home')
            else:
                return HttpResponse("<script>alert('No such 2nd Party Project was Found');location.replace('/users/');</script>")
    else:
        return redirect('user_home')
        
@login_required
def leave_project(request,slug):
    if request.method=="POST":
        projects = Project.objects.filter(slug=slug)
        if projects.exists():
            project = projects[0]
            subscriber = Subscriber.objects.filter(project=project,subscriber=request.user)
            if subscriber.exists():
                subscriber.delete()
                return redirect('user_home')
    
    return Http404()
          
@login_required
def remove_from_project(request,slug):
    context = dict()
    projects = Project.objects.filter(slug=slug,user_id=request.user)
    if not projects.exists():
        raise Http404()
    if request.method == "POST":
        sub_id= request.POST.get('id',None)
        if sub_id is None or sub_id == request.user.id:
            context['errors']="Please Select Proper User For This Operation"
        else:
            try:
                subscriber = Users.objects.get(pk=sub_id)
                project = projects[0]
                sub = Subscriber.objects.get(project=project,subscriber=subscriber)
                sub.delete()
            except Subscriber.DoesNotExist as e:
                context['errors']="The user isn't subscribed to this project"
    
    return redirect("project_details",slug=slug)

@login_required
def transfer_ownership(request,slug):
    context = dict()
    projects = Project.objects.filter(slug=slug,user_id=request.user)
    if not projects.exists():
        raise Http404()
    if request.method == "POST":
        sub_id= request.POST.get('id',None)
        if sub_id is None or sub_id == request.user.id:
            context['errors']="Please Select Proper User For This Operation"
        else:
            try:
                new_subscriber = request.user
                old_subscriber = Users.objects.get(pk=sub_id)
                project = projects[0]
                old_sub = Subscriber.objects.get(project=project,subscriber=old_subscriber)
                old_sub.delete()
                new_sub = Subscriber(project=project,subscriber=new_subscriber)
                new_sub.save();
                project.user_id=old_subscriber;
                project.save()
            except Subscriber.DoesNotExist as e:
                context['errors']="The user isn't subscribed to this project"
    return redirect("user_home")
            
@login_required
def project_details(request,slug):
    context = dict()
    projects = Project.objects.filter(slug=slug).filter(Q(subscriber__subscriber=request.user)|Q(user_id=request.user))
    if not projects.exists():
        raise Http404()
    
    project = projects[0]
    subscribers = Subscriber.objects.filter(project=project)
    #task
    #bugs
    #expenses

    context['project']=project
    context['subscribers']=subscribers
    
    return render(request,'views/projects/project_details.html',context=context)
