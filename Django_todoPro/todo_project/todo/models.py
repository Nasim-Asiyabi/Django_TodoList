from django.db import models
from django.utils import timezone
from django.db.models import QuerySet, Manager
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class TaskQuerySet(QuerySet):
    def expired(self):
        now = timezone.now().date()
        return self.filter(due_date__lt=now, done=False)

    def users_without_tasks(self):
        # Get all users who have at least one task
        users_with_tasks = self.values_list('user__id', flat=True).distinct()
        # Return users who are NOT in the above list
        return User.objects.exclude(id__in=users_with_tasks)


class TaskManager(Manager):
    def get_queryset(self):
        return TaskQuerySet(self.model, using=self._db)

    def expired(self):
        return self.get_queryset().expired()

    def users_without_tasks(self):
        return self.get_queryset().users_without_tasks()


class Task(models.Model):
    # User field for OneToOne relationship with Django User - Question 3
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tasks', null=True, blank=True)
    title = models.CharField(max_length=200)
    due_date = models.DateTimeField()
    due_time = models.TimeField(null=True, blank=True)
    done = models.BooleanField(default=False)

    # Use custom manager
    objects = TaskManager()

    class Meta:
        ordering = ['due_date']

    def __str__(self):
        if self.user:
            return f"{self.title} - {self.user.username}"
        return self.title

    def is_past_due_and_incomplete(self):
        now = timezone.now().date()
        return self.due_date.date() < now and not self.done

    @staticmethod
    def expired_tasks():
        return Task.objects.expired()

    @staticmethod
    def get_users_without_tasks():
        return Task.objects.users_without_tasks()


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    phone = models.CharField(max_length=20, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    birth_date = models.DateField(blank=True, null=True)
    join_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Profile of {self.user.username}"

    def get_task_statistics(self):
        if hasattr(self.user, 'tasks'):
            total = self.user.tasks.count()
            completed = self.user.tasks.filter(done=True).count()
            pending = self.user.tasks.filter(done=False).count()
            return {
                'total': total,
                'completed': completed,
                'pending': pending,
                'completion_rate': round((completed / total * 100) if total > 0 else 0, 2)
            }
        return {'total': 0, 'completed': 0, 'pending': 0, 'completion_rate': 0}


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    if hasattr(instance, 'profile'):
        instance.profile.save()