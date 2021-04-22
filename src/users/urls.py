from django.urls import path
from .views import register,Login,Logout,user_home

urlpatterns = [
    path('',user_home,name="user_home"),
    path('register/',register,name="register"),
    path('login/',Login,name="login"),
    path('logout',Logout,name="logout")
]