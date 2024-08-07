from django.forms import ModelForm
from django.forms import formset_factory

from .models import Board, Task, Column, SubTask

class BoardForm(ModelForm):
    class Meta:
        model = Board
        fields = ['name']
    


class ColumnForm(ModelForm):
    class Meta:
        model = Column
        fields = ['col_name']


# create column formset
ColumnFormSet = formset_factory(ColumnForm)
    