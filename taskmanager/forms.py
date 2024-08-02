from django import forms
from django.forms import formset_factory

from .models import Board, Task, Column, SubTask

class BoardForm(forms.Form):
    name = forms.CharField(label="Name", max_length=50)


class ColumnForm(forms.Form):
    name = forms.CharField(label="Name", max_length=50)
    board = forms.HiddenInput()

# how to dynamically create number?*
# formset to display inside new board form
ColumnFormSet = formset_factory(ColumnForm)    