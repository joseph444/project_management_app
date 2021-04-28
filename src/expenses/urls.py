from django.urls import path
from . import views
urlpatterns = [
    path('create/',views.create_expense,name='create_expense'),
    path('<int:id>/',views.expense_details,name='expense_details'),
    path('<int:id>/edit/',views.edit_details,name='edit_details'),
    path('<int:id>/delete/',views.delete_expense,name='delete_details'),
]