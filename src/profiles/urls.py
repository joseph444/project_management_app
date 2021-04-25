from django.urls import path
from .views import register,myProfile,profile,updateProfile

urlpatterns = [
    path('',myProfile,name="my_profile"),
    path('update/',updateProfile,name="update_profile"),
    path('<str:username>/',profile,name="profile"),
    path('register',register,name="register_profile")

]