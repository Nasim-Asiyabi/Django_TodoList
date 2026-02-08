from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from django.urls import reverse_lazy
from django.utils import timezone
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.db.models import Count
from .models import Task, UserProfile
from .forms import UserRegistrationForm, UserLoginForm, UserProfileForm, TaskForm


# Home View
class HomeView(TemplateView):
    template_name = 'todo/home.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('todo:task_list')
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['expired_count'] = Task.objects.expired().count()
        return context


class CustomLoginView(LoginView):
    template_name = 'todo/login.html'
    authentication_form = UserLoginForm
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('todo:task_list')

    def form_valid(self, form):
        messages.success(self.request, f'Welcome back, {form.get_user().username}!')
        return super().form_valid(form)


class CustomLogoutView(LogoutView):
    next_page = reverse_lazy('todo:login')

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            messages.info(request, f'Goodbye, {request.user.username}!')
        return super().dispatch(request, *args, **kwargs)


class UserRegistrationView(CreateView):
    form_class = UserRegistrationForm
    template_name = 'todo/register.html'
    success_url = reverse_lazy('todo:login')

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('todo:task_list')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        messages.success(self.request, 'Account created successfully! You can now log in.')
        return super().form_valid(form)


class UserProfileView(LoginRequiredMixin, DetailView):
    template_name = 'todo/profile.html'
    context_object_name = 'profile'

    def get_object(self):
        return self.request.user.profile

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        if hasattr(user, 'tasks'):
            context['user_tasks'] = user.tasks.all().order_by('-due_date')[:10]
            stats = user.profile.get_task_statistics()
            context.update(stats)

        return context


class UserProfileUpdateView(LoginRequiredMixin, UpdateView):
    form_class = UserProfileForm
    template_name = 'todo/profile_edit.html'
    success_url = reverse_lazy('todo:profile')

    def get_object(self):
        return self.request.user.profile

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        messages.success(self.request, 'Profile updated successfully!')
        return super().form_valid(form)


class TaskListView(LoginRequiredMixin, ListView):
    model = Task
    template_name = 'todo/index.html'
    context_object_name = 'tasks'

    def get_queryset(self):
        if hasattr(self.request.user, 'tasks'):
            return self.request.user.tasks.all().order_by('due_date')
        return Task.objects.none()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        if hasattr(user, 'tasks'):
            expired_tasks = user.tasks.filter(
                due_date__lt=timezone.now().date(),
                done=False
            )
            context['expired_tasks'] = expired_tasks
            context['expired_count'] = expired_tasks.count()
            context['total_tasks'] = user.tasks.count()

        context['today_date'] = timezone.now()

        if not self.request.session.get('welcome_shown'):
            messages.info(self.request, f'Welcome to your task manager, {user.username}! Here are all your tasks.')
            self.request.session['welcome_shown'] = True

        return context


class TaskCreateView(LoginRequiredMixin, CreateView):
    model = Task
    form_class = TaskForm
    template_name = 'todo/task_form.html'
    success_url = reverse_lazy('todo:task_list')

    def form_valid(self, form):
        task = form.save(commit=False)
        if hasattr(self.request.user, 'tasks'):
            task.user = self.request.user
        task.save()

        messages.success(
            self.request,
            f'✅ Task "{task.title}" has been created successfully! '
            f'Due date: {task.due_date.strftime("%Y-%m-%d")}'
        )
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(
            self.request,
            '❌ Failed to create task. Please check the form for errors.'
        )
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_title'] = 'Create New Task'
        context['submit_text'] = 'Create Task'
        context['cancel_url'] = reverse_lazy('todo:task_list')
        return context


class TaskDetailView(LoginRequiredMixin, DetailView):
    model = Task
    template_name = 'todo/task_detail.html'
    context_object_name = 'task'

    def get_queryset(self):
        if hasattr(self.request.user, 'tasks'):
            return self.request.user.tasks.all()
        return Task.objects.none()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        task = self.get_object()
        context['is_expired'] = task.is_past_due_and_incomplete()

        if task.is_past_due_and_incomplete():
            messages.warning(
                self.request,
                f'⚠️ This task "{task.title}" is past its due date ({task.due_date.strftime("%Y-%m-%d")})!'
            )

        if task.done:
            messages.success(
                self.request,
                f'🎉 Great job! Task "{task.title}" is completed!'
            )

        return context


class TaskUpdateView(LoginRequiredMixin, UpdateView):
    model = Task
    form_class = TaskForm
    template_name = 'todo/task_form.html'

    def get_queryset(self):
        if hasattr(self.request.user, 'tasks'):
            return self.request.user.tasks.all()
        return Task.objects.none()

    def get_success_url(self):
        messages.success(
            self.request,
            f'✅ Task "{self.object.title}" has been updated successfully!'
        )
        return reverse_lazy('todo:task_detail', kwargs={'pk': self.object.pk})

    def form_invalid(self, form):
        messages.error(
            self.request,
            f'❌ Failed to update task "{self.object.title}". Please check the form for errors.'
        )
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_title'] = 'Edit Task'
        context['submit_text'] = 'Update Task'
        context['cancel_url'] = reverse_lazy('todo:task_detail', kwargs={'pk': self.object.pk})
        return context


class TaskDeleteView(LoginRequiredMixin, DeleteView):
    model = Task
    template_name = 'todo/task_confirm_delete.html'
    success_url = reverse_lazy('todo:task_list')

    def get_queryset(self):
        if hasattr(self.request.user, 'tasks'):
            return self.request.user.tasks.all()
        return Task.objects.none()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        task = self.get_object()

        messages.warning(
            self.request,
            f'⚠️ You are about to delete task: "{task.title}". This action cannot be undone!'
        )

        context['task_details'] = {
            'title': task.title,
            'due_date': task.due_date.strftime("%Y-%m-%d"),
            'status': 'Completed' if task.done else 'Not Completed',
            'created_by': task.user.username if task.user else 'Unknown',
        }

        return context

    def delete(self, request, *args, **kwargs):
        task = self.get_object()
        task_title = task.title

        response = super().delete(request, *args, **kwargs)

        # Success message after deletion
        messages.success(
            request,
            f'🗑️ Task "{task_title}" has been permanently deleted successfully!'
        )

        return response


class TaskStatusUpdateView(LoginRequiredMixin, UpdateView):
    model = Task
    template_name = 'todo/task_status_form.html'
    fields = ['done']

    def get_queryset(self):
        if hasattr(self.request.user, 'tasks'):
            return self.request.user.tasks.all()
        return Task.objects.none()

    def get_success_url(self):
        task = self.object

        if task.done:
            messages.success(
                self.request,
                f'🎉 Excellent! Task "{task.title}" has been marked as COMPLETED!'
            )
        else:
            messages.info(
                self.request,
                f'📝 Task "{task.title}" has been marked as NOT COMPLETED.'
            )

        return reverse_lazy('todo:task_detail', kwargs={'pk': task.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        task = self.get_object()

        context['current_status'] = 'Completed' if task.done else 'Not Completed'
        context['new_status'] = 'Not Completed' if task.done else 'Completed'
        context['action_text'] = 'Mark as Not Completed' if task.done else 'Mark as Completed'

        return context


class ExpiredTasksListView(LoginRequiredMixin, ListView):
    template_name = 'todo/expired_tasks.html'
    context_object_name = 'expired_tasks'

    def get_queryset(self):
        if hasattr(self.request.user, 'tasks'):
            return self.request.user.tasks.filter(
                due_date__lt=timezone.now().date(),
                done=False
            ).order_by('due_date')
        return Task.objects.none()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        expired_tasks = self.get_queryset()
        expired_count = expired_tasks.count()

        context['expired_count'] = expired_count
        context['today_date'] = timezone.now()

        if expired_count == 0:
            messages.success(
                self.request,
                '✅ Excellent! You have no expired tasks. Keep up the good work!'
            )
        elif expired_count == 1:
            messages.warning(
                self.request,
                f'⚠️ You have 1 expired task. Consider completing it soon!'
            )
        else:
            messages.warning(
                self.request,
                f'⚠️ You have {expired_count} expired tasks. Consider prioritizing these!'
            )

        return context


class UsersWithoutTasksView(LoginRequiredMixin, ListView):
    template_name = 'todo/users_without_tasks.html'
    context_object_name = 'users'

    def dispatch(self, request, *args, **kwargs):
        """Only allow admin users to access this view"""
        if not request.user.is_superuser:
            messages.error(
                request,
                '❌ Access denied! You must be an administrator to view this page.'
            )
            return redirect('todo:task_list')
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        """Get users without tasks"""
        return Task.objects.users_without_tasks().order_by('username')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        total_users = User.objects.count()
        users_without_tasks = self.get_queryset()
        users_without_count = users_without_tasks.count()

        context['total_users'] = total_users
        context['users_without_tasks_count'] = users_without_count
        context['today_date'] = timezone.now()

        # Add statistics message
        if total_users > 0:
            percentage = round((users_without_count / total_users) * 100, 2)
            context['percentage'] = percentage

            if users_without_count == 0:
                messages.success(
                    self.request,
                    '✅ All registered users have created at least one task!'
                )
            else:
                messages.info(
                    self.request,
                    f'📊 Statistics: {users_without_count} out of {total_users} users ({percentage}%) have not created any tasks.'
                )

        return context