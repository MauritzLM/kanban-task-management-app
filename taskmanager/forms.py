from django.forms import ModelForm
from django.forms import modelformset_factory
from django import forms
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError

from .models import Board, Task, Column, SubTask

class BoardForm(ModelForm):
    class Meta:
        model = Board
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'e.g. Roadmap'}),
        }
        error_messages = {
            'name': {
                'required': _('Can\'t be empty'),
            }
        }


class DeleteBoardForm(ModelForm):
    class Meta:
        model = Board
        fields = []    

class ColumnForm(ModelForm):
    class Meta:
        model = Column
        fields = ['col_name']
        widgets= {
            'col_name': forms.TextInput(attrs={'placeholder': 'e.g Todo'})
            }
        error_messages = {
            'col_name': {
                'required': _('Can\'t be empty'),
            },
        }
    
    # can't submit empty form
    def __init__(self, *arg, **kwarg):
        super(ColumnForm, self).__init__(*arg, **kwarg)
        self.empty_permitted = False    
    
    # custom name field error message
    def clean(self):
        # call clean method
        cleaned_data = super(ColumnForm, self).clean()
        name = cleaned_data.get('col_name')
        
        if not name:
            raise ValidationError(_(''), code='required')     

        return cleaned_data


# formset used in board forms
ColumnFormSet = modelformset_factory(Column,
                                     form=ColumnForm,
                                     extra=0,
                                     can_delete=True,
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
        error_messages = {
            'title': {
                'required': _('Can\'t be empty'),
            },
            'column' : {
                'required': _('You need to select a column')
            }
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


class SubTaskForm(ModelForm):
    class Meta:
        model = SubTask
        fields=['sub_name']
        widgets={'sub_name': forms.TextInput(attrs={'placeholder': 'e.g. Drink coffee and smile.'})}
        error_messages = {
            'sub_name': {
                'required': _('Can\'t be empty'),
            },
        }

     # can't submit empty form
    def __init__(self, *arg, **kwarg):
        super(SubTaskForm, self).__init__(*arg, **kwarg)
        self.empty_permitted = False    
    
    # custom name field error message
    def clean(self):
        # call clean method
        cleaned_data = super(SubTaskForm, self).clean()
        name = cleaned_data.get('sub_name')
        
        if not name:
            raise ValidationError(_(''), code='required')    

        return cleaned_data


# formset used in new task and edit task forms
SubTaskFormSet = modelformset_factory(SubTask,
                                        form=SubTaskForm,
                                        extra=0,
                                        can_delete=True,
                                        widgets={'sub_name': forms.TextInput(attrs={'placeholder': 'e.g. Drink coffee and smile.'})}
                                        )

# formset used in task view (can mark completed)
TaskViewFormSet = modelformset_factory(SubTask,
                                       exclude=['task'],
                                       extra=0,
                                       )  
    