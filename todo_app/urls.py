from . import views
from django.urls import path

urlpatterns = [
    path('', views.loginPage, name='login'),
    path('register/', views.registerPage, name='register'),
    path('logout/', views.logoutUser, name='logout'),
    path('task', views.task, name='task'),
    path('update-task/<str:pk>/', views.updateTask, name='update-task'),
    path('delete-task/<str:pk>/', views.deleteTask, name='delete-task'),
]
