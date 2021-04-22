from django.shortcuts import render,redirect,HttpResponse
from .forms import RegisterForm,LoginForm
from .models import Users
from django.contrib.auth import authenticate,logout,login
from django.contrib.auth.decorators import login_required

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
                return redirect('profile_register')
                
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
def user_home(request):
    return render(request,'views/users/index.html')

