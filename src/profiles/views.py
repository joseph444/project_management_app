from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from .forms import ProfileRegisterForm,roles,ProfileChangeForm
from .models import Profile
from django.http import Http404

@login_required
def register(request):
    if Profile.objects.filter(user_id=request.user.id).exists():
        return redirect('user_home')
    context = {}
    if request.method == "POST":
        print(request.FILES)
        profileForm = ProfileRegisterForm(request.POST,request.FILES)
        if profileForm.is_valid():
            
            username = profileForm.cleaned_data['username']
            pro_pic = request.FILES['pro_picture']
            user_id = request.user
            role = profileForm.cleaned_data['role']
            bio = profileForm.cleaned_data['bio']
            try:
                profile = Profile(user_id=user_id,role=role,username=username,bio=bio)
                profile.pro_picture=pro_pic
                profile.save()
                return redirect('user_home')
                pass
            except Exception as e:
                context['errors']=[
                    "You already have one profile"
                ]
            pass
        else:
            context['errors'] = profileForm.errors
        pass
    context['roles']=roles
    return render(request,"views/profiles/register.html",context=context)


@login_required
def myProfile(request):
    profile = Profile.objects.get(user_id=request.user)
    context={
        "profile":profile,
        "roles":roles
    }
    return render(request,'views/profiles/seeprofile.html',context=context)


def profile(request,username):
    try:
        prof = Profile.objects.get(username=username)
    except Profile.DoesNotExist:
        raise Http404("User Profile not Found")
    context = { 
        "profile":prof,
        "roles":roles
    }
    return render(request,"views/profiles/seeprofile.html",context=context)


@login_required
def updateProfile(request):
    userProfile = Profile.objects.get(user_id=request.user.id)
    if request.FILES.get('pro_picture')!=None:
        prof = ProfileChangeForm(request.POST,request.FILES)
    else:
        prof = ProfileChangeForm(request.POST)
    if prof.is_valid():
        roles = prof.cleaned_data.get('role')
        bio = prof.cleaned_data.get('bio')
        
        try:
            userProfile.role = roles
            userProfile.bio = bio
            if request.FILES.get('pro_picture') !=None:
                pro_pic = request.FILES.get('pro_picture')
                userProfile.pro_picture =pro_pic
            userProfile.save()
            request.session['UPDATE']=True
        except Exception as e:
            print(e)
            request.session['UPDATE']=False
            request.session['REASON'] = "EXCEPTION OCCURED"
    else:
        request.session['UPDATE']=False
        request.session['REASON'] = prof.errors
    return redirect('my_profile')
    
