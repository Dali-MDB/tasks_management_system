from django.urls import path
from . import views

urlpatterns = [
    path('tasks/', views.get_all_tasks, name='get_all_tasks'),
    path('tasks/<int:pk>/', views.task_detail.as_view(), name='task_detail'),
    path('tasks/my-tasks/', views.get_my_assigned_tasks, name='get_my_assigned_tasks'),
    path('tasks/my-managed-tasks/', views.get_my_managed_tasks, name='get_my_managed_tasks'),
    path('tasks/<int:pk>/complete/', views.complete_task, name='complete_task'),    
    path('projects/', views.get_all_projects, name='get_all_projects'),
    path('projects/<int:pk>/', views.project_detail.as_view(), name='project_detail'),
    path('projects/my-projects/', views.get_my_managed_projects, name='get_my_managed_projects'),
    path('projects/my-projects/', views.get_my_projects, name='get_my_projects'),
    path('projects/<int:pk>/add-task/', views.add_task_to_project, name='add_task_to_project'),
    path('projects/<int:pk>/add-contributor/', views.add_contributor_to_project, name='add_contributor_to_project'),
    path('projects/<int:pk>/remove-contributor/', views.remove_contributor_from_project, name='remove_contributor_from_project'),
    path('projects/<int:pk>/remove-task/', views.remove_task_from_project, name='remove_task_from_project'),
    path('projects/<int:pk>/complete/', views.complete_project, name='complete_project'),
    path('projects/<int:pk>/contributor-requests/', views.view_contributor_requests, name='view_contributor_requests'),
    path('contributor-requests/', views.get_all_contributor_requests, name='get_all_contributor_requests'),
    path('contributor-requests/my-requests/', views.get_my_contributor_requests, name='get_my_contributor_requests'),
    path('contributor-requests/<int:pk>/accept/', views.accept_contributor_request, name='accept_contributor_request'),
    path('contributor-requests/<int:pk>/reject/', views.reject_contributor_request, name='reject_contributor_request'),
    path('contributor-requests/<int:pk>/send/', views.send_contributor_request, name='send_contributor_request'),
    path('contributor-requests/<int:pk>/cancel/', views.cancel_contributor_request, name='cancel_contributor_request'),
    
]

