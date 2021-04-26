from django.urls import path,include
from . import views

urlpatterns = [
    path('<slug:slug>',views.project_details,name="project_details"),
    path('<slug:slug>/edit/',views.edit_project,name='edit_project'),
    path('<slug:slug>/delete/',views.delete_project,name='delete_project'),
    path('<slug:slug>/leave/',views.leave_project,name='delete_project'),
    path('<slug:slug>/transfer/',views.transfer_ownership,name='delete_project'),
    path('<slug:slug>/remove/',views.remove_from_project,name='delete_project'),
    path('<slug:slug>/tasks/',include('tasks.urls')),
    path('create/',views.create_project,name='create_project'),
    path('join/',views.join_project,name='join_project')

]