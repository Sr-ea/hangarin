from django.views.generic import ListView, CreateView, UpdateView, DeleteView, TemplateView, DetailView
from .models import Task
from django.contrib.auth.mixins import LoginRequiredMixin
import json
from django.db.models import Q
from django.utils import timezone
from datetime import datetime, timedelta
from django.urls import reverse_lazy
from .models import Task, Category, Priority, Note, SubTask
from .forms import TaskForm, CategoryForm, PriorityForm, NoteForm, SubTaskForm

class TaskDetailView(LoginRequiredMixin,DetailView):
    model = Task
    template_name = 'task/task_detail.html'
    context_object_name = 'task'

class TaskListView(LoginRequiredMixin, ListView):
    model = Task
    context_object_name = 'tasks'
    template_name = 'task/task_list.html'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Get filter parameters
        search_query = self.request.GET.get('q', '')
        category_filter = self.request.GET.get('category', '')
        priority_filter = self.request.GET.get('priority', '')
        status_filter = self.request.GET.get('status', '')
        sort_by = self.request.GET.get('sort', '-created_at')
        
        # Apply search filter
        if search_query:
            queryset = queryset.filter(
                Q(title__icontains=search_query) | 
                Q(description__icontains=search_query)
            )
        
        # Apply category filter - show ONLY tasks from selected category
        if category_filter:
            queryset = queryset.filter(category_id=category_filter)
        
        # Apply priority filter - show ONLY tasks with selected priority
        if priority_filter:
            queryset = queryset.filter(priority_id=priority_filter)
        
        # Apply status filter - show ONLY tasks with selected status
        if status_filter:
            queryset = queryset.filter(status=status_filter)
        
        # Apply sorting
        valid_sorts = ['title', '-title', 'deadline', '-deadline', 'created_at', '-created_at']
        if sort_by in valid_sorts:
            queryset = queryset.order_by(sort_by)
        else:
            queryset = queryset.order_by('-created_at')
        
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Get current filter values
        context['current_search'] = self.request.GET.get('q', '')
        context['current_category'] = self.request.GET.get('category', '')
        context['current_priority'] = self.request.GET.get('priority', '')
        context['current_status'] = self.request.GET.get('status', '')
        context['current_sort'] = self.request.GET.get('sort', '-created_at')
        
        # Add filter options to context
        context['categories'] = Category.objects.all()
        context['priorities'] = Priority.objects.all()
        
        # Define status choices directly in the view
        context['status_choices'] = [
            ('Pending', 'Pending'),
            ('In Progress', 'In Progress'),
            ('Completed', 'Completed')
        ]
        
        return context
    
class TaskCreateView(LoginRequiredMixin,CreateView):
    model = Task
    form_class = TaskForm
    template_name = 'task/task_form.html'
    success_url = reverse_lazy('task-list')

class TaskUpdateView(LoginRequiredMixin,UpdateView):
    model = Task
    form_class = TaskForm
    template_name = 'task/task_form.html'
    success_url = reverse_lazy('task-list')

class TaskDeleteView(LoginRequiredMixin,DeleteView):
    model = Task
    template_name = 'task/task_confirm_delete.html'
    success_url = reverse_lazy('task-list')

# Category Views with Search and Sorting
class CategoryListView(LoginRequiredMixin,ListView):
    model = Category
    context_object_name = 'categories'
    template_name = 'task/category_list.html'
    paginate_by = 10

    def get_queryset(self):
        qs = super().get_queryset()
        query = self.request.GET.get('q')
        
        if query:
            qs = qs.filter(name__icontains=query)
        return qs

    def get_ordering(self):
        allowed = ['name', '-name', 'created_at', '-created_at']
        sort_by = self.request.GET.get('sort_by', 'name')
        if sort_by in allowed:
            return sort_by
        return 'name'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_query'] = self.request.GET.get('q', '')
        context['current_sort'] = self.request.GET.get('sort_by', 'name')
        context['total_categories'] = Category.objects.count()
        
        context['sort_options'] = [
            {'value': 'name', 'label': 'Name A-Z'},
            {'value': '-name', 'label': 'Name Z-A'},
            {'value': '-created_at', 'label': 'Newest First'},
            {'value': 'created_at', 'label': 'Oldest First'}
        ]
        
        return context

class CategoryCreateView(LoginRequiredMixin,CreateView):
    model = Category
    form_class = CategoryForm
    template_name = 'task/category_form.html'
    success_url = reverse_lazy('category-list')

class CategoryUpdateView(LoginRequiredMixin,UpdateView):
    model = Category
    form_class = CategoryForm
    template_name = 'task/category_form.html'
    success_url = reverse_lazy('category-list')

class CategoryDeleteView(LoginRequiredMixin,DeleteView):
    model = Category
    template_name = 'task/category_confirm_delete.html'
    success_url = reverse_lazy('category-list')

# Priority Views with Search and Sorting
class PriorityListView(LoginRequiredMixin,ListView):
    model = Priority
    context_object_name = 'priorities'
    template_name = 'task/priority_list.html'
    paginate_by = 10

    def get_queryset(self):
        qs = super().get_queryset()
        query = self.request.GET.get('q')
        
        if query:
            qs = qs.filter(
                Q(name__icontains=query) |
                Q(color__icontains=query)  # Removed description, added color
            )
        return qs

    def get_ordering(self):
        allowed = ['name', '-name', 'created_at', '-created_at']
        sort_by = self.request.GET.get('sort_by', 'name')
        if sort_by in allowed:
            return sort_by
        return 'name'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_query'] = self.request.GET.get('q', '')
        context['current_sort'] = self.request.GET.get('sort_by', 'name')
        context['total_priorities'] = Priority.objects.count()
        
        context['sort_options'] = [
            {'value': 'name', 'label': 'Name A-Z'},
            {'value': '-name', 'label': 'Name Z-A'},
            {'value': '-created_at', 'label': 'Newest First'},
            {'value': 'created_at', 'label': 'Oldest First'}
        ]
        
        return context

class PriorityCreateView(LoginRequiredMixin,CreateView):
    model = Priority
    form_class = PriorityForm
    template_name = 'task/priority_form.html'
    success_url = reverse_lazy('priority-list')

class PriorityUpdateView(LoginRequiredMixin,UpdateView):
    model = Priority
    form_class = PriorityForm
    template_name = 'task/priority_form.html'
    success_url = reverse_lazy('priority-list')

class PriorityDeleteView(LoginRequiredMixin,DeleteView):
    model = Priority
    template_name = 'task/priority_confirm_delete.html'
    success_url = reverse_lazy('priority-list')

# Note Views with Search and Sorting
class NoteListView(LoginRequiredMixin,ListView):
    model = Note
    context_object_name = 'notes'
    template_name = 'task/note_list.html'
    paginate_by = 10

    def get_queryset(self):
        qs = super().get_queryset()
        query = self.request.GET.get('q')
        
        if query:
            qs = qs.filter(
                Q(content__icontains=query) |
                Q(task__title__icontains=query)
            )
        return qs

    def get_ordering(self):
        allowed = ['-created_at', 'created_at', 'task__title']
        sort_by = self.request.GET.get('sort_by', '-created_at')
        if sort_by in allowed:
            return sort_by
        return '-created_at'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_query'] = self.request.GET.get('q', '')
        context['current_sort'] = self.request.GET.get('sort_by', '-created_at')
        context['total_notes'] = Note.objects.count()
        
        context['sort_options'] = [
            {'value': '-created_at', 'label': 'Newest First'},
            {'value': 'created_at', 'label': 'Oldest First'},
            {'value': 'task__title', 'label': 'Task Title'}
        ]
        
        return context

class NoteCreateView(LoginRequiredMixin,CreateView):
    model = Note
    form_class = NoteForm
    template_name = 'task/note_form.html'
    success_url = reverse_lazy('note-list')

class NoteUpdateView(LoginRequiredMixin,UpdateView):
    model = Note
    form_class = NoteForm
    template_name = 'task/note_form.html'
    success_url = reverse_lazy('note-list')

class NoteDeleteView(LoginRequiredMixin,DeleteView):
    model = Note
    template_name = 'task/note_confirm_delete.html'
    success_url = reverse_lazy('note-list')

# SubTask Views with Search and Sorting
class SubTaskListView(LoginRequiredMixin,ListView):
    model = SubTask
    context_object_name = 'subtasks'
    template_name = 'task/subtask_list.html'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Get filter parameters
        search_query = self.request.GET.get('q', '')
        status_filter = self.request.GET.get('status', '')
        sort_by = self.request.GET.get('sort', '-created_at')
        
        # Apply search filter - only on existing fields
        if search_query:
            queryset = queryset.filter(
                Q(title__icontains=search_query) |
                Q(task__title__icontains=search_query)  # Only search on title and parent task title
            )
        
        # Apply status filter - show ONLY subtasks with selected status
        if status_filter:
            queryset = queryset.filter(status=status_filter)
        
        # Apply sorting
        valid_sorts = ['-created_at', 'created_at', 'title', '-title', 'status', 'deadline', '-deadline', 'task__title']
        if sort_by in valid_sorts:
            queryset = queryset.order_by(sort_by)
        else:
            queryset = queryset.order_by('-created_at')
        
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Get current filter values
        context['search_query'] = self.request.GET.get('q', '')
        context['current_status'] = self.request.GET.get('status', '')
        context['current_sort'] = self.request.GET.get('sort', '-created_at')
        
        # Define status choices
        context['status_choices'] = [
            ('Pending', 'Pending'),
            ('In Progress', 'In Progress'),
            ('Completed', 'Completed')
        ]
        
        return context

class SubTaskDetailView(LoginRequiredMixin,DetailView):
    model = SubTask
    template_name = 'subtask_detail.html'
    context_object_name = 'subtask'

class SubTaskCreateView(LoginRequiredMixin,CreateView):
    model = SubTask
    form_class = SubTaskForm
    template_name = 'task/subtask_form.html'
    success_url = reverse_lazy('subtask-list')

class SubTaskUpdateView(LoginRequiredMixin,UpdateView):
    model = SubTask
    form_class = SubTaskForm
    template_name = 'task/subtask_form.html'
    success_url = reverse_lazy('subtask-list')

class SubTaskDeleteView(LoginRequiredMixin,DeleteView):
    model = SubTask
    template_name = 'task/subtask_confirm_delete.html'
    success_url = reverse_lazy('subtask-list')

# Enhanced Home Page View with Dashboard Statistics
class HomePageView(LoginRequiredMixin,TemplateView):
    template_name = "home.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        today = timezone.now().date()
        
        # Basic statistics
        context['total_tasks'] = Task.objects.count()
        context['pending_tasks'] = Task.objects.filter(status='Pending').count()
        context['in_progress_tasks'] = Task.objects.filter(status='In Progress').count()
        context['completed_tasks'] = Task.objects.filter(status='Completed').count()
        context['overdue_tasks'] = Task.objects.filter(
            deadline__lt=today, 
            status__in=['Pending', 'In Progress']
        ).count()
        
        # Additional dashboard statistics
        context['total_categories'] = Category.objects.count()
        context['total_priorities'] = Priority.objects.count()
        context['total_notes'] = Note.objects.count()
        context['total_subtasks'] = SubTask.objects.count()
        
        # Progress statistics
        if context['total_tasks'] > 0:
            context['completion_rate'] = round((context['completed_tasks'] / context['total_tasks']) * 100, 1)
        else:
            context['completion_rate'] = 0
            
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
        ).select_related('priority')
        
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