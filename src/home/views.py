from django.shortcuts import render




def home(request):
    return render(request,"views/home/index.html")


def about(request):
    return render(request,"views/home/about.html")
