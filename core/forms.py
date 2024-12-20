from django import forms
from .models import Task

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = [
            'title', 'description', 'category', 
            'location', 'urgency', 'required_skills', 
            'budget', 'status'
        ]
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'urgency': forms.NumberInput(attrs={'min': 1, 'max': 5}),
        }
