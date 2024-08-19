from django.test import TestCase
from taskmanager.models import Board, Column, Task, SubTask

# board model
class BoardModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Board.objects.create(name='Platform Launch')
    
    def test_name_label(self):
        board = Board.objects.get(name='Platform Launch')
        field_label = board._meta.get_field('name').verbose_name
        self.assertEqual(field_label, 'name')


    def test_save(self):
        board = Board.objects.get(name='Platform Launch')
        self.assertEqual(board.save(), board)    
    

    def test_get_absolute_url(self):
        board = Board.objects.get(name='Platform Launch')
        # This will also fail if the urlconf is not defined.
        self.assertEqual(board.get_absolute_url(), f'/taskmanager/board/{board.id}')


# column model
class ColumnModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        board = Board.objects.create(name='Platform Launch')
        Column.objects.create(col_name='todo', board=board)

    def test_name_label(self):
        column = Column.objects.get(col_name='todo')
        field_label = column._meta.get_field('col_name').verbose_name
        self.assertEqual(field_label, 'col name')


# task model
class TaskModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        board = Board.objects.create(name='Platform Launch')
        column = Column.objects.create(col_name='todo', board=board)
        Task.objects.create(title='build ui', description='some text', column=column)

    def test_name_label(self):
        task = Task.objects.get(title="build ui")
        field_label = task._meta.get_field('title').verbose_name
        self.assertEqual(field_label, 'title')

    def test_save(self):
        task = Task.objects.get(title='build ui')
        self.assertEqual(task.save(), task)    


# subtask model
class SubtaskModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        board = Board.objects.create(name='Platform Launch')
        column = Column.objects.create(col_name='todo', board=board)
        task = Task.objects.create(title='build ui', description='some text', column=column)
        SubTask.objects.create(sub_name='brainstorm ideas', task=task)

    def test_name_label(self):
        subtask = SubTask.objects.get(sub_name='brainstorm ideas')
        field_label = subtask._meta.get_field('sub_name').verbose_name
        self.assertEqual(field_label, 'sub name')    
