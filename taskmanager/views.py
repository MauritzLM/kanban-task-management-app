from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse

from .helpers import build_new_formset
from .models import Board, Column
from .forms import BoardForm, ColumnFormSet

# index page
def index(request):
    all_boards = Board.objects.all()
    return render(request, 'index.html', context={'all_boards': all_boards})

# view board
def board_detail_view(request, id):
    board = get_object_or_404(Board, id=id)
    all_boards = Board.objects.all()

    return render(request, 'components/board_detail.html', context={'board': board, 'all_boards': all_boards})

# create board
def board_form(request):
    if request.method == 'POST':
        board_form = BoardForm(request.POST)
        column_formset = ColumnFormSet(request.POST)

        if board_form.is_valid() and column_formset.is_valid():
            # save board and get object
            created_board = board_form.save()  

            # set column id
            columns = column_formset.save(commit=False)
            for col in columns:
                col.board = created_board
                col.save()

            return HttpResponseRedirect(reverse('index'))
        
        # validate column fields*

    else:
        board_form = BoardForm()
        column_formset = ColumnFormSet(queryset=Column.objects.none())
            
    return render(request, 'components/board_form.html', context={'board_form': board_form, 'formset': column_formset, 'title': 'New'})


# edit board
def edit_board(request, id):
    board_to_edit = get_object_or_404(Board, id=id)
    # create form from board instance
    board_form = BoardForm(instance=board_to_edit)

    # create formset from columns add initial data
    board_columns = ColumnFormSet(queryset=Column.objects.filter(board=id))

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

            return HttpResponseRedirect(reverse('index'))
        else:
            return render(request, 'components/edit_board_form.html', context={'title': 'edit',
            'board_form': board_form,
            'board_to_edit': board_to_edit,
            'formset': board_columns})
    else:
        context = {
            'title': 'edit',
            'board_form': board_form,
            'board_to_edit': board_to_edit,
            'formset': board_columns
        }
        
    return render(request, 'components/edit_board_form.html', context)

# column form
def column_form(request, current_total_formsets):
    new_formset = build_new_formset(ColumnFormSet(), current_total_formsets)
    context = {
        'new_formset': new_formset,
        'new_total_formsets': current_total_formsets + 1,
    }
    
    return render(request, 'components/column_form.html', context)

def delete_board(request, id):
    board_to_delete = get_object_or_404(Board, id=id)
    return render(request, 'components/delete_board_form.html', context={'board': board_to_delete})