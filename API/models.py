from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    # is_admin = models.BooleanField(default=False)
    
    def __str__(self):
        return self.username
    

class Category(models.Model):
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name

    
class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)
    
    def __str__(self):
        return self.name
 
    
class Task(models.Model):
    STATUS_CHOICES = (
        ('TODO', 'To Do'), 
        ('INPR', 'In Progress'), 
        ('DONE', 'Done'),        
    )
    PRIORITY_CHOICES = (
        ('LOW', 'Low'), 
        ('MED', 'Medium'), 
        ('HIGH', 'High'),      
    )
    title = models.CharField(max_length=255)
    description = models.TextField()
    status = models.CharField(max_length=4, choices=STATUS_CHOICES, default='TODO')
    priority = models.CharField(max_length=4, choices=PRIORITY_CHOICES, default='MED')
    due_date = models.DateTimeField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tasks')
    category = models.ForeignKey('Category', on_delete=models.SET_NULL, null=True, blank=True, related_name='tasks')
    
    def __str__(self):
        return self.title
    
    
class TaskFile(models.Model):
    file_path = models.FileField(upload_to='task_files/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='files')
    
    def __str__(self):
        return f"File for Task: {self.task.title} at {self.file_path}"

      
class TaskTag(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='task_tags')
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE, related_name='task_tags')
    
    def __str__(self):
        return f"Task: {self.task.title} (Tag: {self.tag.name})"

