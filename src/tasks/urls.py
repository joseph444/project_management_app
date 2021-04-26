from django.urls import path
from . import views
urlpatterns = [
    path('create/',views.create_task,name="create_task"),
    path('<int:id>/toggle-done/',views.toggle_is_done,name="toggle_done_task"),
    path('<int:id>/edit/',views.edit_task,name="edit-task"),
    path('<int:id>/delete/',views.delete_task,name="delete-task"),
    path('<int:id>/',views.task_details,name="task-details")
]