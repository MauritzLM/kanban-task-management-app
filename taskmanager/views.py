from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse

from .models import Board
from .forms import BoardForm, ColumnForm
# Create your views here.

def index(request):
    all_boards = Board.objects.all()
    return render(request, 'index.html', context={'all_boards': all_boards})

def board_detail_view(request, id):
    board = get_object_or_404(Board, id=id)
    all_boards = Board.objects.all()

    return render(request, 'components/board_detail.html', context={'board': board, 'all_boards': all_boards})

def new_board(request):
    if request.method == 'POST':
        form = BoardForm(request.POST)
        if form.is_valid():
            board = form.save()
            return HttpResponseRedirect(reverse('index'))
    else:
        form = BoardForm()
    return render(request, 'components/board_form.html', {
        'form': form,
    })

def new_column(request, id):
    if request.method == 'POST':
        form = ColumnForm(request.POST)
        if form.is_valid():
            column = form.save()
            return HttpResponseRedirect(reverse('index'))
    else:
        form = ColumnForm()
        
    return render(request, 'components/column_form.html', {
        'form': form
    })