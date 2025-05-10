from django.db import models
from django.contrib.auth.models import User

class Task(models.Model):
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    assigned_to = models.ForeignKey(User, on_delete=models.CASCADE, related_name='assigned_tasks')
    title = models.CharField(max_length=200)
    description = models.TextField()
    completed = models.BooleanField(default=False)
    deadline = models.DateTimeField()

    def __str__(self):
        return self.title
    
class Project(models.Model):
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField()
    tasks = models.ManyToManyField(Task, related_name='projects')
    contributors = models.ManyToManyField(User, related_name='projects')
    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField()
    completed = models.BooleanField(default=False)

    def __str__(self):
        return self.title
    
class ContributorRequest(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    accepted = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username
