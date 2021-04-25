from django.shortcuts import render,redirect,HttpResponse
from .forms import RegisterForm,LoginForm
from .models import Users
from django.contrib.auth import authenticate,logout,login
from django.contrib.auth.decorators import login_required
from profiles.models import Profile
from projects.views import all_projects
#TODO: create view functions for update profile, resetPassword


def register(request):
    context ={}
    if request.user.is_authenticated:
        return redirect('user_home')
        pass
    else:
        if request.method == "POST":
            print(request.POST)
            registerForm = RegisterForm(request.POST)
            if registerForm.is_valid():
                #this will save the user
                user = registerForm.save()
                print("hello")
                login(request,user)
                return redirect('register_profile')
                
            else:
                context['errors'] = registerForm.errors

        
        return render(request,"views/users/register.html",context)
        pass




def Login(request):
    content = {}
    if request.user.is_authenticated:
        return redirect('user_home')
        pass
    else:
        
        if request.method=="POST":
            loginForm = LoginForm(request.POST)
            if loginForm.is_valid():
                email = loginForm.cleaned_data['email']
                password = loginForm.cleaned_data['password']
                user = authenticate(email=email,password=password)
                login(request,user)
                return redirect('user_home')
            else:
                content = loginForm.errors
            

        return render(request,"views/users/login.html",content)



@login_required
def Logout(request):
    if request.method == "POST":
        logout(request)
        return redirect('home')
    return HttpResponse("Method Not Allowed")


@login_required
def user_home(request,errors=None):
    context = dict()
    if Profile.objects.filter(user_id=request.user.id).exists():
        if request.GET.get('join_project') is not None :
            context['template']='join_project'
            
        elif request.GET.get('create_project') is not None :
            context['template']='create_project'
            
        else:
            context['template']='all_project'
            context['datas'] = all_projects(request)
        if errors is not None:
            context['template']='create_project'
            context['errors']=errors
        context['template_url'] = 'views/projects/'+context['template']+'.html'
        return render(request,'views/users/index.html',context=context)
    
    return redirect('register_profile')

