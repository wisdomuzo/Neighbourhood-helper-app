from django.urls import path
from . import views

app_name = 'tasks'  # Namespace for your app
urlpatterns = [
    path('tasks/', views.task_list, name='task_list'),
    path('tasks/create/', views.create_task, name='create_task'),
    path('tasks/<int:task_id>/', views.task_detail, name='task_detail'),
    path('tasks/<int:task_id>/edit/', views.edit_task, name='edit_task'),  # Add this URL
    path('tasks/<int:task_id>/delete/', views.delete_task, name='delete_task'),  # Add this URL
]
