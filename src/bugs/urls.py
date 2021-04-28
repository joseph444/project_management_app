from django.urls import path
from . import views
urlpatterns = [
    path('create/',views.create,name="register-bug"),
    path('<int:id>/',views.show,name="show-bug"),
    path('<int:id>/edit/',views.edit,name="edit-bug"),
    path('<int:id>/toggle-close/',views.toggle,name='toggle-bug'),
    path('<int:id>/delete/',views.delete,name="delete")
]