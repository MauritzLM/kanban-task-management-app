from django.forms import ModelForm
from django.forms import modelformset_factory

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
ColumnFormSet = modelformset_factory(Column, exclude=['board', 'id'])
    