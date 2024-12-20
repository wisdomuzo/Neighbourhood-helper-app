from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Task
from .forms import TaskForm
from django.db.models import Q  # Use Q for flexible filtering
from django.core.paginator import Paginator
from django.contrib import messages

# Task Creation view
@login_required
def create_task(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.posted_by = request.user  # Ensure task is associated with the current user
            task.save()
            return redirect('tasks:task_list')  # Use namespaced URL
    else:
        form = TaskForm()
    return render(request, 'create_task.html', {'form': form})


# Task List View with Pagination and Filtering
@login_required
def task_list(request):
    query = request.GET.get('q', '')
    category = request.GET.get('category', '')

    # Flexible filtering
    tasks = Task.objects.all()
    if query:
        tasks = tasks.filter(Q(title__icontains=query) | Q(description__icontains=query))
    if category:
        tasks = tasks.filter(category=category)

    # Pagination
    tasks = tasks.order_by('id')
    paginator = Paginator(tasks, 10)  # Show 10 tasks per page
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)

    return render(request, 'task_list.html', {
        'tasks': page_obj.object_list,
        'page_obj': page_obj,
        'query': query,
        'category': category,
    })


# Task Detail View
@login_required
def task_detail(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    return render(request, 'task_detail.html', {'task': task})

# Task edit view
@login_required
def edit_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    
    if request.user != task.posted_by:
        # Redirect if the user doesn't own the task
        return redirect('task_list')

    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('tasks:task_detail', task_id=task.id)  # Redirect to the task detail page
    else:
        form = TaskForm(instance=task)

    return render(request, 'edit_task.html', {'form': form, 'task': task})

# Delete Task View

@login_required
def delete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    
    if request.user != task.posted_by:
        # Redirect if the user doesn't own the task
        return redirect('task_list')

    task.delete()
    messages.success(request, 'Task successfully deleted.')
    return redirect('task_list')  # Redirect back to task list after deletion
