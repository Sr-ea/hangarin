from django.urls import path
from .views import (
    # Task Views
    TaskListView, TaskCreateView, TaskUpdateView, TaskDeleteView,TaskDetailView,
    # Category Views
    CategoryListView, CategoryCreateView, CategoryUpdateView, CategoryDeleteView,
    # Priority Views
    PriorityListView, PriorityCreateView, PriorityUpdateView, PriorityDeleteView,
    # Note Views
    NoteListView, NoteCreateView, NoteUpdateView, NoteDeleteView,
    # SubTask Views
    SubTaskListView, SubTaskDetailView, SubTaskCreateView, SubTaskUpdateView, SubTaskDeleteView,
)

urlpatterns = [
    # Task URLs
    path('<int:pk>/view/', TaskDetailView.as_view(), name='task-detail'),
    path('', TaskListView.as_view(), name='task-list'),
    path('add/', TaskCreateView.as_view(), name='task-add'),
    path('<int:pk>/', TaskUpdateView.as_view(), name='task-update'),
    path('<int:pk>/delete/', TaskDeleteView.as_view(), name='task-delete'),
    
    # Category URLs
    path('categories/', CategoryListView.as_view(), name='category-list'),
    path('categories/add/', CategoryCreateView.as_view(), name='category-add'),
    path('categories/<int:pk>/', CategoryUpdateView.as_view(), name='category-update'),
    path('categories/<int:pk>/delete/', CategoryDeleteView.as_view(), name='category-delete'),
    
    # Priority URLs
    path('priorities/', PriorityListView.as_view(), name='priority-list'),
    path('priorities/add/', PriorityCreateView.as_view(), name='priority-add'),
    path('priorities/<int:pk>/', PriorityUpdateView.as_view(), name='priority-update'),
    path('priorities/<int:pk>/delete/', PriorityDeleteView.as_view(), name='priority-delete'),
    
    # Note URLs
    path('notes/', NoteListView.as_view(), name='note-list'),
    path('notes/add/', NoteCreateView.as_view(), name='note-add'),
    path('notes/<int:pk>/', NoteUpdateView.as_view(), name='note-update'),
    path('notes/<int:pk>/delete/', NoteDeleteView.as_view(), name='note-delete'),
    
    # SubTask URLs
    path('subtasks/', SubTaskListView.as_view(), name='subtask-list'),
     path('subtasks/<int:pk>/', SubTaskDetailView.as_view(), name='subtask-detail'),
    path('subtasks/add/', SubTaskCreateView.as_view(), name='subtask-add'),
    path('subtasks/<int:pk>/', SubTaskUpdateView.as_view(), name='subtask-update'),
    path('subtasks/<int:pk>/delete/', SubTaskDeleteView.as_view(), name='subtask-delete'),
]