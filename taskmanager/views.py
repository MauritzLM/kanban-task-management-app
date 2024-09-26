import json

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from .helpers import build_new_formset
from .models import Board, Column, Task, SubTask
from .forms import BoardForm, ColumnFormSet, DeleteBoardForm, TaskForm, SubTaskFormSet, TaskViewForm, TaskViewFormSet, DeleteTaskForm

# index page
def index(request):
    # if user is logged in get user boards
    if request.user.is_authenticated:
        user_boards = Board.objects.filter(user=request.user)
        
        return render(request, 'base.html', context={'user_boards': user_boards}) 
    
    return render(request, 'base.html')
     
# sidebar
def get_sidebar(request):
    # if user is logged in get user boards
    if request.user.is_authenticated:
        all_boards = Board.objects.filter(user=request.user)

        return render(request, 'components/sidebar.html', context={'all_boards': all_boards})

    return render(request, 'components/sidebar.html')

# BOARDS (login required)
# view board
@login_required
def board_detail_view(request, id):
    # improve db queries*
    
    # get board
    board = get_object_or_404(Board, id=id)
    # get columns
    columns = Column.objects.filter(board=board)

    return render(request, 'components/board_detail.html', context={'board': board, 'columns': columns})

# create board
@login_required
def board_form(request):
    if request.method == 'POST':
        board_form = BoardForm(request.POST)
        column_formset = ColumnFormSet(request.POST)

        if board_form.is_valid() and column_formset.is_valid():
            # save board and get object
            board_name = board_form.cleaned_data['name']
            board_user = request.user

            created_board = Board(name=board_name, user=board_user)
            saved_board = created_board.save()  

            columns = column_formset.save(commit=False)
            for col in columns:
                # dont save empty forms
                # set column id
                col.board = saved_board
                col.save() 
            
            return HttpResponse(
                status=204,
                headers={
                    'HX-Trigger': json.dumps({
                        "boardCreated": None,
                        "showMessage": f"{saved_board.name} updated."
                    })
                }
            )
            
        
        # update column formset to include only not empty ones
    else:
        board_form = BoardForm()
        column_formset = ColumnFormSet(queryset=Column.objects.none())
   
            
    return render(request, 'components/forms/board_form.html', context={'board_form': board_form, 'formset': column_formset, 'title': 'Add New Board'})


# edit board
@login_required
def edit_board(request, id):
    board_to_edit = get_object_or_404(Board, id=id)
    
    if request.method == 'POST':
        board_form = BoardForm(request.POST, instance=board_to_edit)
        column_formset = ColumnFormSet(request.POST)

        if board_form.is_valid() and column_formset.is_valid():
            board_form.save()
            # new columns / updated columns*
            # set column id
            columns = column_formset.save(commit=False)
            
            # delete columns selected for delete
            for obj in column_formset.deleted_objects:
                obj.delete()

            # save / update columns
            for col in columns:
                col.board = board_to_edit
                col.save()

            return HttpResponse(
                status=204,
                headers={
                    'HX-Trigger': json.dumps({
                        "boardChanged": None,
                        "showMessage": f"{board_to_edit.name} updated."
                    })
                }
            )

    else:
        # create form from board instance
        board_form = BoardForm(instance=board_to_edit)
        # create formset from board columns
        column_formset = ColumnFormSet(queryset=Column.objects.filter(board=id).order_by('col_name'))
       
    return render(request, 'components/forms/edit_board_form.html', context={'title': 'Edit Board', 'board_form': board_form, 'board_to_edit': board_to_edit, 'formset': column_formset})


# column form
@login_required
def column_form(request, current_total_formsets):
    new_formset = build_new_formset(ColumnFormSet(), current_total_formsets)
    context = {
        'new_formset': new_formset,
        'new_total_formsets': current_total_formsets + 1,
    }

    return render(request, 'components/forms/column_form.html', context) 

   

# delete board
@login_required
def delete_board(request, id):
    board_to_delete = get_object_or_404(Board, id=id)

    if request.method == 'POST':
        delete_form = DeleteBoardForm(request.POST, instance=board_to_delete)

        if delete_form.is_valid():
            board_to_delete.delete()

        return HttpResponseRedirect(reverse('index'))
    
    else:
        context = {
            'board_to_delete': board_to_delete,
            'delete_form': DeleteBoardForm(instance=board_to_delete)
        }
       
    return render(request, 'components/forms/delete_board_form.html', context)

# TASKS
# task view
@login_required
def task_view(request, id, t_id):
    task = get_object_or_404(Task, id=t_id)
    board = get_object_or_404(Board, id=id)

    # handle post request
    if request.method == 'POST':
        task_form = TaskViewForm(request.POST, instance=task)
        subtask_formset = TaskViewFormSet(request.POST)

        if task_form.is_valid() and subtask_formset.is_valid():

            updated_task = task_form.save()

            # save subtasks
            subtasks = subtask_formset.save(commit=False)
            for sub in subtasks:
                sub.task = updated_task
                sub.save()

            # response
            return HttpResponse(
                status=204,
                headers={
                    'HX-Trigger': json.dumps({
                        "taskChanged": None,
                        "showMessage": f"{task.title} updated."
                    })
                }
            )
    
    else:
        task_form = TaskViewForm(instance=task)
        subtask_formset = TaskViewFormSet(queryset=SubTask.objects.filter(task=t_id).order_by('-is_completed'))

    # only add columns from selected board
    task_form.fields['column'].queryset = Column.objects.filter(board=id)

    return render(request, 'components/task_view.html', context={'board': board,'task': task, 'task_form': task_form, 'subtask_formset': subtask_formset})
    

# create new task
@login_required
def new_task(request, id):
    board = get_object_or_404(Board, id=id)
    
    if request.method == 'POST':
        task_form = TaskForm(request.POST)
        subtask_formset = SubTaskFormSet(request.POST)

        if task_form.is_valid() and subtask_formset.is_valid():
            # save task and get object
            created_task = task_form.save()  

            # save subtasks
            subtasks = subtask_formset.save(commit=False)
            for sub in subtasks:
                sub.task = created_task
                sub.save()

            # redirect*
            return HttpResponse(
                status=204,
                headers={
                    'HX-Trigger': json.dumps({
                        "taskCreated": None,
                        "showMessage": f"{created_task.title} created."
                    })
                }
            )

    else:
        task_form = TaskForm()
        subtask_formset = SubTaskFormSet(queryset=SubTask.objects.none())

    # only add columns from selected board
    task_form.fields['column'].queryset = Column.objects.filter(board=id)    

    return render(request, 'components/forms/task_form.html', context={'board': board,
            'task_form': task_form, 'subtask_formset': subtask_formset, 'title': 'Add New Task'})

# edit task
@login_required
def edit_task(request, id, t_id):
    board = get_object_or_404(Board, id=id)
    task_to_edit = get_object_or_404(Task, id=t_id)

    if request.method == 'POST':
        task_form = TaskForm(request.POST, instance=task_to_edit)
        subtask_formset = SubTaskFormSet(request.POST)

        if task_form.is_valid() and subtask_formset.is_valid():
            # save task
            task_form.save()

            # new subtasks / updated subtasks
            subtasks = subtask_formset.save(commit=False)
            
            # delete subtasks selected for delete
            for obj in subtask_formset.deleted_objects:
                obj.delete()

            # save / update subtasks
            for sub in subtasks:
                sub.task = task_to_edit
                sub.save()

            return HttpResponse(
                status=204,
                headers={
                    'HX-Trigger': json.dumps({
                        "taskChanged": None,
                        "showMessage": f"{task_to_edit.title} updated."
                    })
                }
            )
    
    else:
        task_form = TaskForm(instance=task_to_edit)
        subtask_formset = SubTaskFormSet(queryset=SubTask.objects.filter(task=t_id).order_by('sub_name'))

    # only add columns from selected board
    task_form.fields['column'].queryset = Column.objects.filter(board=id)

    return render(request, 'components/forms/edit_task_form.html', context={'board': board,
            'task_form': task_form, 'subtask_formset': subtask_formset, 'title': 'Edit Task', 'task': task_to_edit})    

# delete task
@login_required
def delete_task(request, t_id):
    task_to_delete = get_object_or_404(Task, id=t_id)

    if request.method == 'POST':
        delete_form = DeleteTaskForm(request.POST, instance=task_to_delete)

        if delete_form.is_valid():
            task_to_delete.delete()
            
            return HttpResponse(
                status=204,
                headers={
                    'HX-Trigger': json.dumps({
                        "taskChanged": None,
                        "showMessage": "task deleted"
                    })
                }
            )
           
    
    else:
        context = {
            'task_to_delete': task_to_delete,
            'delete_form': DeleteTaskForm(instance=task_to_delete)
        }
       
    return render(request, 'components/forms/delete_task_form.html', context)


# subtask form
@login_required
def subtask_form(request, current_total_formsets):
    new_formset = build_new_formset(SubTaskFormSet(), current_total_formsets)
    context = {
        'new_formset': new_formset,
        'new_total_formsets': current_total_formsets + 1,
    }
    
    return render(request, 'components/forms/subtask_form.html', context)  