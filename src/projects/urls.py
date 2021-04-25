from django.urls import path
from .views import create_project,edit_project,delete_project,join_project,leave_project

urlpatterns = [
    path('<slug:slug>/edit/',edit_project,name='edit_project'),
    path('<slug:slug>/delete/',delete_project,name='delete_project'),
    path('<slug:slug>/leave/',leave_project,name='delete_project'),
    path('create/',create_project,name='create_project'),
    path('join/',join_project,name='join_project')

]