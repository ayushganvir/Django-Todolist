from django.urls import path

from . import views
from .views import EditTodo

urlpatterns = [
    path('', views.login, name='todo-login'),
    path('index/', views.index, name='todo-index'),
    path('contact_me/', views.contact_me, name='todo-contact-me'),
    path('register/', views.register, name='todo-register'),
    path('logout/', views.t_logout, name='todo-logout'),
    path('title_detail/<int:todo_id>/', views.title_detail, name='todo-title-detail'),
    path('delete/<int:todo_id>/', views.delete, name='todo-delete'),
    path('completed/<int:todo_id>/', views.completed, name='todo-completed'),
    path('edit/<int:todo_id>', EditTodo.as_view(), name='todo-edit'),

]
