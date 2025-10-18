from django.views.generic import ListView, CreateView, UpdateView, DeleteView, TemplateView, DetailView
from .models import Task
import json
from django.utils import timezone
from datetime import datetime,  timedelta
from django.urls import reverse_lazy
from .models import Task, Category, Priority, Note, SubTask
from .forms import TaskForm, CategoryForm, PriorityForm, NoteForm, SubTaskForm

class TaskDetailView(DetailView):
    model = Task
    template_name = 'task/task_detail.html'
    context_object_name = 'task'
    
class TaskListView(ListView):
    model = Task
    context_object_name = 'tasks'
    template_name = 'task/task_list.html'
    paginate_by = 10
    ordering = ['-created_at']

class TaskCreateView(CreateView):
    model = Task
    form_class = TaskForm
    template_name = 'task/task_form.html'
    success_url = reverse_lazy('task-list')

class TaskUpdateView(UpdateView):
    model = Task
    form_class = TaskForm
    template_name = 'task/task_form.html'
    success_url = reverse_lazy('task-list')

class TaskDeleteView(DeleteView):
    model = Task
    template_name = 'task/task_confirm_delete.html'
    success_url = reverse_lazy('task-list')

# Category Views
class CategoryListView(ListView):
    model = Category
    context_object_name = 'categories'
    template_name = 'task/category_list.html'
    paginate_by = 10

class CategoryCreateView(CreateView):
    model = Category
    form_class = CategoryForm
    template_name = 'task/category_form.html'
    success_url = reverse_lazy('category-list')

class CategoryUpdateView(UpdateView):
    model = Category
    form_class = CategoryForm
    template_name = 'task/category_form.html'
    success_url = reverse_lazy('category-list')

class CategoryDeleteView(DeleteView):
    model = Category
    template_name = 'task/category_confirm_delete.html'
    success_url = reverse_lazy('category-list')

# Priority Views
class PriorityListView(ListView):
    model = Priority
    context_object_name = 'priorities'
    template_name = 'task/priority_list.html'
    paginate_by = 10

class PriorityCreateView(CreateView):
    model = Priority
    form_class = PriorityForm
    template_name = 'task/priority_form.html'
    success_url = reverse_lazy('priority-list')

class PriorityUpdateView(UpdateView):
    model = Priority
    form_class = PriorityForm
    template_name = 'task/priority_form.html'
    success_url = reverse_lazy('priority-list')

class PriorityDeleteView(DeleteView):
    model = Priority
    template_name = 'task/priority_confirm_delete.html'
    success_url = reverse_lazy('priority-list')

# Note Views
class NoteListView(ListView):
    model = Note
    context_object_name = 'notes'
    template_name = 'task/note_list.html'
    paginate_by = 10
    ordering = ['-created_at']

class NoteCreateView(CreateView):
    model = Note
    form_class = NoteForm
    template_name = 'task/note_form.html'
    success_url = reverse_lazy('note-list')

class NoteUpdateView(UpdateView):
    model = Note
    form_class = NoteForm
    template_name = 'task/note_form.html'
    success_url = reverse_lazy('note-list')

class NoteDeleteView(DeleteView):
    model = Note
    template_name = 'task/note_confirm_delete.html'
    success_url = reverse_lazy('note-list')

# SubTask Views
class SubTaskListView(ListView):
    model = SubTask
    context_object_name = 'subtasks'
    template_name = 'task/subtask_list.html'
    paginate_by = 10
    ordering = ['-created_at']

class SubTaskCreateView(CreateView):
    model = SubTask
    form_class = SubTaskForm
    template_name = 'task/subtask_form.html'
    success_url = reverse_lazy('subtask-list')

class SubTaskUpdateView(UpdateView):
    model = SubTask
    form_class = SubTaskForm
    template_name = 'task/subtask_form.html'
    success_url = reverse_lazy('subtask-list')

class SubTaskDeleteView(DeleteView):
    model = SubTask
    template_name = 'task/subtask_confirm_delete.html'
    success_url = reverse_lazy('subtask-list')

# Home Page View
class HomePageView(TemplateView):
    template_name = "home.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        today = timezone.now().date()
        
        # Basic statistics
        context['total_tasks'] = Task.objects.count()
        context['pending_tasks'] = Task.objects.filter(status='Pending').count()
        context['completed_tasks'] = Task.objects.filter(status='Completed').count()
        context['overdue_tasks'] = Task.objects.filter(
            deadline__lt=today, 
            status__in=['Pending', 'In Progress']
        ).count()
        context['current_year'] = today.year
        context['current_month'] = today.strftime("%B")
        
        # Today's tasks
        context['todays_tasks'] = Task.objects.filter(
            deadline__date=today
        ).order_by('deadline')
        
        # Upcoming tasks (next 7 days)
        next_week = today + timedelta(days=7)
        context['upcoming_tasks'] = Task.objects.filter(
            deadline__date__range=[today + timedelta(days=1), next_week],
            status__in=['Pending', 'In Progress']
        ).order_by('deadline')[:5]
        
        # Calendar data
        calendar_data, tasks_by_date = self.get_enhanced_calendar_data(today)
        context['calendar_data'] = json.dumps(calendar_data)
        context['tasks_by_date'] = json.dumps(tasks_by_date)
        
        return context
    
    def get_enhanced_calendar_data(self, today):
        # Get tasks for the current month
        start_of_month = today.replace(day=1)
        if today.month == 12:
            end_of_month = today.replace(year=today.year + 1, month=1, day=1) - timedelta(days=1)
        else:
            end_of_month = today.replace(month=today.month + 1, day=1) - timedelta(days=1)
        
        monthly_tasks = Task.objects.filter(
            deadline__date__range=[start_of_month, end_of_month]
        ).select_related('priority')  # Optimize query
        
        # Create enhanced tasks by date dictionary
        tasks_by_date = {}
        for task in monthly_tasks:
            date_key = task.deadline.date().isoformat()
            if date_key not in tasks_by_date:
                tasks_by_date[date_key] = []
            
            tasks_by_date[date_key].append({
                'title': task.title,
                'priority_name': task.priority.name,
                'priority_color': task.priority.color,
                'status': task.status,
                'id': task.id
            })
        
        # Calendar structure
        calendar_data = {
            'year': today.year,
            'month': today.month,
            'month_name': today.strftime("%B"),
            'today': today.isoformat()
        }
        
        return calendar_data, tasks_by_date