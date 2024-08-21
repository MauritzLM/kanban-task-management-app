from django.forms import ModelForm
from django.forms import modelformset_factory
from django import forms
from django.utils.translation import gettext_lazy as _

from .models import Board, Task, Column, SubTask

class BoardForm(ModelForm):
    class Meta:
        model = Board
        fields = ['name']

class DeleteBoardForm(ModelForm):
    class Meta:
        model = Board
        fields = []    


class ColumnForm(ModelForm):
    class Meta:
        model = Column
        fields = ['col_name']


# create column formset
ColumnFormSet = modelformset_factory(Column,
                                     exclude=['board', 'id'],
                                     extra=0,
                                     can_delete=True,
                                     widgets={'col_name': forms.TextInput(attrs={'placeholder': 'e.g Todo'})},  
                                    )

# for create new and edit
class TaskForm(ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'column']
        labels = {
            'column': _('Status'),
        }
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'e.g. Take a 15 minute break'}),
            'description': forms.Textarea(attrs={'placeholder': 'e.g. Its always good to take a break. This 15 minute break will recharge the batteries a little.'}),
        }
        

class DeleteTaskForm(ModelForm):
    class Meta:
        model = Task
        fields = []        

# for viewing task
class TaskViewForm(ModelForm):
    class Meta:
        model = Task
        fields = ['column']
        labels = {
            'column': _('Status'),
        }


SubTaskFormSet = modelformset_factory(SubTask,
                                       exclude=['task', 'id', 'is_completed'],
                                        extra=0,
                                        can_delete=True,
                                        widgets={'sub_name': forms.TextInput(attrs={'placeholder': 'e.g. Drink coffee and smile.'})},
                                        )

TaskViewFormSet = modelformset_factory(SubTask,
                                       exclude=['task', 'id'],
                                       extra=0,
                                       widgets={'sub_name': forms.TextInput(attrs={'placeholder': 'e.g. Drink coffee and smile.'})},
                                       )  
    