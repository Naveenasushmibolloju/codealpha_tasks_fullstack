from django import forms
from .models import Task
from .models import Comment

class TaskForm(forms.ModelForm):

    class Meta:
        model = Task
        fields = [
            'title',
            'description',
            'project',
            'assigned_to',
            'priority',
            'status',
            'due_date',
        ]

        widgets = {
            'due_date': forms.DateInput(attrs={'type': 'date'})
        }


class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ['message']