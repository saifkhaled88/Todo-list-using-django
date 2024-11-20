from django.db import models
from django.contrib.auth.models import User
class Task(models.Model):
    
    title = models.CharField(max_length=50)

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('in-progress', 'In Progress'),
        ('completed', 'Completed'),
    ]
    
    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
    ]
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='medium')
    user = models.ForeignKey(User, on_delete=models.CASCADE,default=1)
    #created = models.DateTimeField(auto_now_add=True)


    class Meta:
       ordering = ['priority']


    def __str__(self):
        return self.title