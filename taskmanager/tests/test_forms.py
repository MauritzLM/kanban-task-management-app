from django.test import TestCase

from taskmanager.forms import BoardForm, ColumnForm, TaskForm, TaskViewForm, DeleteBoardForm, DeleteTaskForm,SubTaskForm, ColumnFormSet, SubTaskFormSet, TaskViewFormSet
from taskmanager.models import Board, Column, Task, SubTask

# board form
class BoardFormTest(TestCase):
    # test form fields
    def test_empty_boardform(self):
        form = BoardForm()
        self.assertIn('name', form.fields)

    # test valid form
    def test_valid_boardform(self):
        form_data = {'name': 'Platform Launch'}
        form = BoardForm(data=form_data)
        self.assertTrue(form.is_valid())
    
    # test invalid form
    def test_invalid_boardform(self):
        form_data = {'name': ''}
        form = BoardForm(data=form_data)
        self.assertFalse(form.is_valid())
    
    # test required fields
    def test_required_fields(self):
        form_data = {'name': ''}
        form = BoardForm(data=form_data)
        errors_name = form['name'].errors.as_data()
        self.assertEqual(len(errors_name), 1)
        self.assertEqual(errors_name[0].code, 'required')
        # error message (better way to get value?)*
        self.assertEqual(''.join(form.errors['name']), 'Can\'t be empty')

# delete form
class DeleteBoardFormTest(TestCase):
    def test_valid_delete_board_form(self):
        form = DeleteBoardForm({})
        self.assertTrue(form.is_valid())    

# column form
class ColumnFormTest(TestCase):
    def test_empty_columnform(self):
        form = ColumnForm()
        self.assertIn('col_name', form.fields)

# column formset
class ColumnFormsetTest(TestCase):
    # test validation
    def test_valid_column_formset(self):
        form_data = {'form-TOTAL_FORMS': '2','form-INITIAL_FORMS': '0', 'form-0-col_name': 'todo', 'form-1-col_name': 'doing'}
        formset = ColumnFormSet(form_data)
        self.assertTrue(formset.is_valid())
    
    # test empty form should not validate ( empty forms are permitted atm )
    # def test_invalid_column_formset(self):
    #     form_data = {'form-TOTAL_FORMS': '1','form-INITIAL_FORMS': '0', 'form-0-col_name': ''}
    #     formset = ColumnFormSet(form_data)
    #     errors = formset.errors
    #     self.assertFalse(formset.is_valid()) 
    #     # error msg
    #     self.assertEqual(errors[0]['col_name'][0], 'Can\'t be empty')
           

# task forms
class TaskFormTest(TestCase):
    # test form fields
    def test_empty_taskform(self):
        form = TaskForm()
        self.assertIn('title', form.fields)
        self.assertIn('description', form.fields)
        self.assertIn('column', form.fields)

    # test column label 
    def test_taskform_colunm_label(self):
        form = TaskForm()
        self.assertTrue(form.fields['column'].label is None or form.fields['column'].label == 'Status')

    # test valid form
    def test_valid_taskform(self):
        board = Board.objects.create(name='Platform Launch')
        column = Column.objects.create(col_name='todo', board=board)
        form_data = {'title': 'brainstorm', 'description': 'hello', 'column': column}
        form = TaskForm(data=form_data)
        self.assertTrue(form.is_valid())


    # test invalid form
    def test_invalid_taskform(self):
        form_data = {'title': 'brainstorm', 'description': 'hello', 'column': ''}
        form = TaskForm(data=form_data)
        self.assertFalse(form.is_valid())
    
    # test not required fields
    def test_description_not_required(self):
        board = Board.objects.create(name='Platform Launch')
        column = Column.objects.create(col_name='todo', board=board)
        form_data = {'title': 'brainstorm', 'description': '', 'column': column}
        form = TaskForm(data=form_data)
        self.assertTrue(form.is_valid())

    # test errors     
    def test_required_fields(self):
        # missing title and column
        form_data = {'title': '', 'description': '', 'column': ''}
        form = TaskForm(data=form_data)
        # title error
        errors_title = form['title'].errors.as_data()
        self.assertEqual(len(errors_title), 1)
        self.assertEqual(errors_title[0].code, 'required')
        # error message
        self.assertEqual(''.join(form.errors['title']), 'Can\'t be empty')

        # column error
        errors_column = form['column'].errors.as_data()
        self.assertEqual(len(errors_column), 1)
        self.assertEqual(errors_column[0].code, 'required')
        # error message
        self.assertEqual(''.join(form.errors['column']), 'You need to select a column')

    # test placeholder text


# task view form
class TaskViewFormTest(TestCase):
    # test form fields
    def test_empty_taskviewform(self):
        form = TaskViewForm()
        self.assertIn('column', form.fields)

    # test column label
    def test_taskviewform_colunm_label(self):
        form = TaskViewForm()
        self.assertTrue(form.fields['column'].label is None or form.fields['column'].label == 'Status')


    # test valid form
    def test_valid_form(self):
        board = Board.objects.create(name='Platform Launch')
        column = Column.objects.create(col_name='todo', board=board)
        form_data = {'column': column}
        form = TaskViewForm(data=form_data)
        self.assertTrue(form.is_valid())


    # test invalid form
    def test_invalid_taskviewform(self):
        form_data = {'column': ''}
        form = TaskViewForm(data=form_data)
        self.assertFalse(form.is_valid())


# subtask forms
class SubTaskFormTest(TestCase):
    # test form fields
    def test_empty_subtaskform(self):
        form = SubTaskForm()
        self.assertIn('sub_name', form.fields)

# subtask formset
class SubTaskFormsetTest(TestCase):
    # test validation
    def test_valid_subtask_formset(self):
        form_data = {'form-TOTAL_FORMS': '2','form-INITIAL_FORMS': '0', 'form-0-sub_name': 'drink coffee', 'form-1-sub_name': 'smile'}
        formset = SubTaskFormSet(form_data)
        self.assertTrue(formset.is_valid())
    
    # test empty form should not validate
    # def test_invalid_subtask_formset(self):
    #     form_data = {'form-TOTAL_FORMS': '1','form-INITIAL_FORMS': '0', 'form-0-sub_name': ''}
    #     formset = SubTaskFormSet(form_data)
    #     errors = formset.errors
    #     self.assertFalse(formset.is_valid())
    #     # error msg
    #     self.assertEqual(errors[0]['sub_name'][0], 'Can\'t be empty')

# taskview formset
class TaskViewFormsetTest(TestCase):
    # fields, is completed
    # test validation
    def test_valid_taskview_formset(self):
        formset = TaskViewFormSet({'form-TOTAL_FORMS': '2','form-INITIAL_FORMS': '0', 'form-0-sub_name': 'drink coffee', 'form-0-is_completed': 'True', 'form-1-sub_name': 'smile', 'form-0-is_completed': 'False'})
        self.assertTrue(formset.is_valid())
