from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse

from .models import Board, Column
from .forms import BoardForm, ColumnForm

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
        column_form = ColumnForm(request.POST)
        if board_form.is_valid() and column_form.is_valid():
            created_board = board_form.save()
            # get id from saved board
            # how to set?*
            column_form.cleaned_data['board'] = created_board.id 
            column_form.save() 
            return HttpResponseRedirect(reverse('index'))
    else:
        context = {
            'title': 'new',
            'board_form': BoardForm(),
            'column_form': ColumnForm()
        }
        
    return render(request, 'components/board_form.html', context)

# edit board
def edit_board(request, id):
    board_to_edit = get_object_or_404(Board, id=id)
    board_columns = Column.objects.filter(board=id)

    if request.method == 'POST':
        board_form = BoardForm(request.POST)
        column_form = ColumnForm(request.POST)
        if board_form.is_valid() and column_form.is_valid():
            board_form.save()
            column_form.save()
            return HttpResponseRedirect(reverse('index'))
    else:
        context = {
            'title': 'edit',
            'board_form': BoardForm(),
            'column_form': ColumnForm(),
            'board_to_edit': board_to_edit,
            'board_columns': board_columns
        }
        
    return render(request, 'components/edit_board_form.html', context)

# column form
def column_form(request):
    return render(request, 'components/column_form.html', context={'column_form': ColumnForm()})