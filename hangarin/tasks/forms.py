from django import forms
from .models import Task, Category, Priority, Note, SubTask

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = '__all__'
        widgets = {
            'deadline': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'description': forms.Textarea(attrs={'rows': 3}),
        }

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = '__all__'

class PriorityForm(forms.ModelForm):
    class Meta:
        model = Priority
        fields = '__all__'
        widgets = {
            'color': forms.TextInput(attrs={
                'type': 'color', 
                'class': 'form-control form-control-color',
                'title': 'Choose a color for this priority'
            }),
        }

class NoteForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = '__all__'
        widgets = {
            'content': forms.Textarea(attrs={'rows': 4}),
        }

class SubTaskForm(forms.ModelForm):
    class Meta:
        model = SubTask
        fields = '__all__'