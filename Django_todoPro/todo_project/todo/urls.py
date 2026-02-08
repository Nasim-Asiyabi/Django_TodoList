from django.urls import path
from .views import (
    # Auth views - Question 3
    HomeView, CustomLoginView, CustomLogoutView,
    UserRegistrationView, UserProfileView, UserProfileUpdateView,

    # Task views
    TaskListView, TaskDetailView, TaskCreateView,
    TaskUpdateView, TaskDeleteView, TaskStatusUpdateView,

    # Special views for Questions 1 and 2
    ExpiredTasksListView, UsersWithoutTasksView
)

app_name = 'todo'

urlpatterns = [
    # Home URL
    path('', HomeView.as_view(), name='home'),

    # Auth URLs - Question 3
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('profile/', UserProfileView.as_view(), name='profile'),
    path('profile/edit/', UserProfileUpdateView.as_view(), name='profile_edit'),

    # Task URLs
    path('tasks/', TaskListView.as_view(), name='task_list'),
    path('tasks/create/', TaskCreateView.as_view(), name='task_create'),
    path('tasks/<int:pk>/', TaskDetailView.as_view(), name='task_detail'),
    path('tasks/<int:pk>/edit/', TaskUpdateView.as_view(), name='task_edit'),
    path('tasks/<int:pk>/delete/', TaskDeleteView.as_view(), name='task_delete'),
    path('tasks/<int:pk>/update-status/', TaskStatusUpdateView.as_view(), name='task_update_status'),

    # Special URLs for Questions
    path('expired-tasks/', ExpiredTasksListView.as_view(), name='expired_tasks_list'),  # Question 1
    path('users-without-tasks/', UsersWithoutTasksView.as_view(), name='users_without_tasks'),  # Question 2
]