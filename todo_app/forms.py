from django import forms
from django.forms import ModelForm
from .models import Task

class LoginForm(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput())


class TaskForm(ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'status', 'priority']