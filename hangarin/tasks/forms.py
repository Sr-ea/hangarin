from django import forms
from .models import Task, Category, Priority, Note, SubTask

class TaskForm(forms.ModelForm):
    notes = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={'rows': 4}),
        help_text="Optional notes for this task"
    )
    
    subtasks = forms.CharField(
        required=False,
        widget=forms.HiddenInput(),  # We'll handle subtasks via JavaScript
        help_text="Optional subtasks"
    )
    
    class Meta:
        model = Task
        fields = ['title', 'description', 'status', 'priority', 'category', 'deadline', 'notes']
    
    def save(self, commit=True):
        task = super().save(commit=commit)
        
        # Handle notes
        if self.cleaned_data.get('notes'):
            task.notes = self.cleaned_data['notes']
            if commit:
                task.save()
        
        # Handle subtasks (you'll need to parse from form data)
        # This is a simplified example - you might need to adjust based on your needs
        subtasks_data = self.data.getlist('subtasks')
        if subtasks_data:
            # Clear existing subtasks
            task.subtasks.all().delete()
            
            # Add new subtasks
            for subtask_title in subtasks_data:
                if subtask_title.strip():  # Only create if not empty
                    Subtask.objects.create(
                        task=task,
                        title=subtask_title.strip(),
                        completed=False
                    )
        
        return task

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
        