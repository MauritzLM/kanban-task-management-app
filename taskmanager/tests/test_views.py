from django.test import TestCase, Client
from django.urls import reverse
from taskmanager.models import Board, Column, Task, SubTask
import uuid
from urllib.parse import urlencode

from django.contrib.auth import get_user_model
User = get_user_model()


# test: url, reverse(name), correct template used, context, setup
# test auth: user logged in, user not logged in
# test views with forms -> initial display, failed validation, successful validation

# index view
class IndexViewTest(TestCase):

    def test_url_exists(self):
        response = self.client.get('/taskmanager/')
        self.assertEqual(response.status_code, 200)

    def test_url_accessible_by_name(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)    
    
    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'base.html')

# get sidebar view
class SiderbarViewTest(TestCase):

    def test_url_exists(self):
        response = self.client.get('/taskmanager/board/sidebar')
        self.assertEqual(response.status_code, 200)

    def test_url_accessible_by_name(self):
        response = self.client.get(reverse('sidebar'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('sidebar'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'components/sidebar.html')        
    
    # with logged in user
    def test_view_with_loggedin_user(self):
        # create user
        test_user1 = User.objects.create_user(username='testuser1', password='1X<ISRUkw+tuK')
        test_user1.save()

        # create user boards
        board_1 = Board.objects.create(name='platform launch', user=test_user1)
        board_2 = Board.objects.create(name='roadmap', user=test_user1)

        # log user in
        login = self.client.login(username='testuser1', password='1X<ISRUkw+tuK')

        response = self.client.get(reverse('sidebar'))
        self.assertTrue('all_boards' in response.context)
        self.assertEqual(len(response.context['all_boards']), 2)

# AUTH VIEWS

# board detail -> url, template, logged in, not logged in
class BoardDetailViewTest(TestCase):
    def setUp(self):
        test_user1 = User.objects.create_user(username='testuser1', password='1X<ISRUkw+tuK')
        test_user1.save()
        
        # create user board
        board_1 = Board.objects.create(name='platform launch', user=test_user1)

    def test_redirect_if_user_not_logged_in(self):
        response = self.client.get(reverse('board-detail', args=[str(1)]))
        self.assertRedirects(response, '/taskmanager/accounts/login?next=/taskmanager/board/1')

    def test_url_exists(self):
        login = self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        # get created board to use in url request
        test_board = Board.objects.get(name='platform launch')
        response = self.client.get(f'/taskmanager/board/{test_board.id}')
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        login = self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        test_board = Board.objects.get(name='platform launch')
        response = self.client.get(reverse('board-detail', args=[str(test_board.id)]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'components/board_detail.html')

    def test_view_with_board_selected(self):
        login = self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        test_board = Board.objects.get(name='platform launch')
        response = self.client.get(reverse('board-detail', args=[str(test_board.id)]))
        selected_board = response.context['board']

        self.assertEqual(response.status_code, 200)
        self.assertTrue('board' in response.context)
        self.assertEqual(selected_board.name, 'platform launch')

    def test_HTTP404_for_invalid_board_if_logged_in(self):
        test_uid = uuid.uuid4()
        login = self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        response = self.client.get(reverse('board-detail', args=[str(test_uid)]))
        self.assertEqual(response.status_code, 404) 
               

# board form -> url, template, logged in, not logged in, validation
class NewBoardViewTest(TestCase):
    def setUp(self):
        test_user1 = User.objects.create_user(username='testuser1', password='1X<ISRUkw+tuK')
        test_user1.save()

    def test_redirect_if_user_not_logged_in(self):
        response = self.client.get(reverse('new-board'))
        self.assertRedirects(response, '/taskmanager/accounts/login?next=/taskmanager/board/new-board')
    
    def test_url_exists(self):
        login = self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        response = self.client.get('/taskmanager/board/new-board')
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        login = self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        
        response = self.client.get(reverse('new-board'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'components/forms/board_form.html')

    # initial display -> empty board form, column formset
    def test_initial_forms(self):
        login = self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        response = self.client.get(reverse('new-board'))
        
        self.assertEqual(response.status_code, 200)
        self.assertTrue('board_form' in response.context)
        self.assertTrue('formset' in response.context)
        self.assertTrue('title' in response.context)
        # empty formset
        self.assertEqual(len(response.context['formset']), 0)

    # post req
    # invalid form errors
    def test_invalid_boardform(self):
        login = self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        # empty name
        response = self.client.post(reverse('new-board'), {'name': ''})
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response.context['board_form'], 'name', 'Can\'t be empty')
    
    # test that empty formset form does not get saved*
    
    # ( not using this atm )
    # def test_invalid_formset(self):
    #     login = self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
    #     board_form_data = {'name': 'platform launch'}
    #     formset_data = {
    #     # management_form data
    #     'form-INITIAL_FORMS': '0',
    #     'form-TOTAL_FORMS': '1',
    #     'form-MAX_NUM_FORMS': '',
    #     # empty col_name
    #     'form-0-col_name': '',
    #     }

    #     response = self.client.post(reverse('new-board'), {**board_form_data, **formset_data})
    #     self.assertEqual(response.status_code, 200)
    #     self.assertFormError(response.context['formset'][0], 'col_name', 'Can\'t be empty')  

    # valid form redirects
    def test_valid_form_redirects_to_index(self):
        login = self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        board_form_data = {'name': 'platform launch'}
        formset_data = {
        # management_form data
        'form-INITIAL_FORMS': '0',
        'form-TOTAL_FORMS': '1',
        'form-MAX_NUM_FORMS': '',

        'form-0-col_name': 'todo',
        }
        response = self.client.post(reverse('new-board'), {**board_form_data, **formset_data}, follow=True)
        self.assertRedirects(response, reverse('index'))
        

# edit board form -> url, template, logged in, not logged in, validation
class EditBoardViewTest(TestCase):
    def setUp(self):
        test_user1 = User.objects.create_user(username='testuser1', password='1X<ISRUkw+tuK')
        test_user1.save()
        
        # create board
        test_board = Board.objects.create(name='platform launch', user=test_user1)

        # two columns for this board
        test_column_1 = Column.objects.create(col_name='todo', board=test_board)
        test_column_2 = Column.objects.create(col_name='done', board=test_board)

    def test_redirect_if_user_not_logged_in(self):
        test_board = Board.objects.get(name='platform launch')
        response = self.client.get(reverse('edit-board', args=[str(test_board.id)]))
        self.assertRedirects(response, f'/taskmanager/accounts/login?next=/taskmanager/board/{test_board.id}/edit-board')
    
    def test_url_exists(self):
        test_board = Board.objects.get(name='platform launch')
        login = self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        response = self.client.get(f'/taskmanager/board/{test_board.id}/edit-board')
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        login = self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        test_board = Board.objects.get(name='platform launch')
        response = self.client.get(reverse('edit-board', args=[str(test_board.id)]))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'components/forms/edit_board_form.html')    
    

    def test_initial_form_values(self):
        login = self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        test_board = Board.objects.get(name='platform launch')
        response = self.client.get(reverse('edit-board', args=[str(test_board.id)]))
        
        self.assertEqual(response.status_code, 200)
        # response context
        self.assertTrue('board_form' in response.context)
        self.assertTrue('board_to_edit' in response.context)
        self.assertTrue('formset' in response.context)
        # board form initial values
        self.assertEqual(response.context['board_form'].initial['name'], 'platform launch')
        # column formset len & initial values
        self.assertEqual(len(response.context['formset']), 2)
        self.assertEqual(response.context['formset'][0].initial['col_name'], 'done')
        self.assertEqual(response.context['formset'][1].initial['col_name'], 'todo')

    # post
    def test_valid_form_redirects_to_index(self):
        login = self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        test_board = Board.objects.get(name='platform launch')
        # change name
        board_form_data = {'name': 'roadmap'}
        # delete doing column
        formset_data = {
        # management_form data
        'form-INITIAL_FORMS': '0',
        'form-TOTAL_FORMS': '2',
        'form-MAX_NUM_FORMS': '',
        'form-0-DELETE': '',
        'form-0-col_name': 'todo',
        'form-1-DELETE': 'on',
        'form-1-col_name': 'doing',
        }
        response = self.client.post(reverse('edit-board', args=[str(test_board.id)]), {**board_form_data, **formset_data}, follow=True)
        self.assertRedirects(response, reverse('index'))
        

    def test_invalid_form_errors(self):  
        login = self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        test_board = Board.objects.get(name='platform launch')
        # empty name
        board_form_data = {'name': ''}
        # empty 3rd column name
        formset_data = {
        # management_form data
        'form-INITIAL_FORMS': '0',
        'form-TOTAL_FORMS': '3',
        'form-MAX_NUM_FORMS': '',
        'form-0-DELETE': '',
        'form-0-col_name': 'todo',
        'form-1-DELETE': 'on',
        'form-1-col_name': 'doing',
        'form-2-col_name': ''
        }
        response = self.client.post(reverse('edit-board', args=[str(test_board.id)]), {**board_form_data, **formset_data})
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response.context['formset'][2], 'col_name', 'Can\'t be empty')
        self.assertFormError(response.context['board_form'], 'name', 'Can\'t be empty')



# column form -> url, template, logged in, not logged in, validation
class ColumnFormViewTest(TestCase):
    def setUp(self):
        test_user1 = User.objects.create_user(username='testuser1', password='1X<ISRUkw+tuK')
        test_user1.save()

    def test_redirect_if_user_not_logged_in(self):
        response = self.client.get(reverse('add-column', args=[str(1)]))
        self.assertRedirects(response, '/taskmanager/accounts/login?next=/taskmanager/board/column/1')

    def test_url_exists(self):
        login = self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        response = self.client.get('/taskmanager/board/column/1') 
        self.assertEqual(response.status_code, 200)
        

    def test_view_uses_correct_template(self):
        login = self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        response = self.client.get(reverse('add-column', args=[str(1)]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'components/forms/column_form.html') 
        

    def test_number_of_formsets(self):
        login = self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        response = self.client.get(reverse('add-column', args=[str(2)]))

        self.assertEqual(response.status_code, 200)
        self.assertTrue('new_formset' in response.context)
        self.assertTrue('new_total_formsets' in response.context)
        # new formset total
        self.assertEqual(response.context['new_total_formsets'], 3)             


# delete board -> url, template, logged in, not logged in
class DeleteBoardViewTest(TestCase):
    def setUp(self):
        test_user1 = User.objects.create_user(username='testuser1', password='1X<ISRUkw+tuK')
        test_user1.save()
        
        # create board
        test_board = Board.objects.create(name='platform launch', user=test_user1)

        # column
        test_column_1 = Column.objects.create(col_name='todo', board=test_board)

    def test_redirect_if_user_not_logged_in(self):
        test_board = Board.objects.get(name='platform launch')
        response = self.client.get(reverse('delete-board', args=[str(test_board.id)]))
        self.assertRedirects(response, f'/taskmanager/accounts/login?next=/taskmanager/board/{test_board.id}/delete-board')

    def test_url_exists(self):
        login = self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        test_board = Board.objects.get(name='platform launch')
        response = self.client.get(f'/taskmanager/board/{test_board.id}/delete-board')
        self.assertEqual(response.status_code, 200)


    def test_view_uses_correct_template(self):
        login = self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        test_board = Board.objects.get(name='platform launch')
        response = self.client.get(reverse('delete-board', args=[str(test_board.id)]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'components/forms/delete_board_form.html')
        
    # post
    def test_success_redirects_to_index(self):
        login = self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        test_board = Board.objects.get(name='platform launch')
        response = self.client.post(reverse('delete-board', args=[str(test_board.id)]), {'name': 'platform launch'}, follow=True)
        self.assertRedirects(response, reverse('index'))


# task view -> url, template, logged in, not logged in, validation
class TaskViewTest(TestCase):
    def setUp(self):
        test_user1 = User.objects.create_user(username='testuser1', password='1X<ISRUkw+tuK')
        test_user1.save()
        
        # create board
        test_board = Board.objects.create(name='platform launch', user=test_user1)

        # two columns for this board
        test_column_1 = Column.objects.create(col_name='todo', board=test_board)
        test_column_2 = Column.objects.create(col_name='done', board=test_board)

        # setup task
        test_task = Task.objects.create(title='brainstorm', description='30 min session', column=test_column_1)

        # two subtasks
        test_subtask_1 = SubTask.objects.create(sub_name='make coffee', is_completed='True', task=test_task)
        test_subtask_2 = SubTask.objects.create(sub_name='drink coffee', is_completed='False', task=test_task)
        test_subtask_3 = SubTask.objects.create(sub_name='smile', is_completed='True', task=test_task)

    # board/<str:id>/view-task/<str:t_id>
    def test_taskview_redirect_if_user_not_logged_in(self):
        test_board = Board.objects.get(name='platform launch')
        test_task = Task.objects.get(title='brainstorm')
        response = self.client.get(reverse('view-task', args=[str(test_board.id), str(test_task.id)]))
        self.assertRedirects(response, f'/taskmanager/accounts/login?next=/taskmanager/board/{test_board.id}/view-task/{test_task.id}')

    def test_taskview_url_exists(self):
        login = self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        test_board = Board.objects.get(name='platform launch')
        test_task = Task.objects.get(title='brainstorm')
        response = self.client.get(f'/taskmanager/board/{test_board.id}/view-task/{test_task.id}')
        self.assertEqual(response.status_code, 200)
        

    def test_taskview_uses_correct_template(self):
        login = self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        test_board = Board.objects.get(name='platform launch')
        test_task = Task.objects.get(title='brainstorm')
        response = self.client.get(reverse('view-task', args=[str(test_board.id), str(test_task.id)]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'components/task_view.html')


    def test_initial_taskview_form_values(self):
        # current status(column), formset length
        login = self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        test_board = Board.objects.get(name='platform launch')
        test_task = Task.objects.get(title='brainstorm')
        test_column = Column.objects.get(col_name='todo')
        response = self.client.get(reverse('view-task', args=[str(test_board.id), str(test_task.id)]))

        self.assertTrue('task' in response.context)
        self.assertTrue('task_form' in response.context)
        self.assertTrue('subtask_formset' in response.context)
        # task form initial values
        self.assertEqual(response.context['task_form'].initial['column'], test_column.id)
        # subtask formset len & initial values (ordered by is_completed => true values first)
        self.assertEqual(len(response.context['subtask_formset']), 3)
        self.assertEqual(response.context['subtask_formset'][0].initial['sub_name'], 'make coffee')
        self.assertEqual(response.context['subtask_formset'][1].initial['sub_name'], 'smile')
        self.assertEqual(response.context['subtask_formset'][2].initial['sub_name'], 'drink coffee')
        

    # post
    def test_valid_taskview_form_redirects_to_index(self):
        login = self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        test_board = Board.objects.get(name='platform launch')
        test_task = Task.objects.get(title='brainstorm')

        task_form_data = {'column': 'done'}
        subtask_formset_data = {
            # management_form data
        'form-INITIAL_FORMS': '0',
        'form-TOTAL_FORMS': '2',
        'form-MAX_NUM_FORMS': '',
        'form-0-sub_name': 'make coffee',
        'form-0-is_completed': 'True',
        'form-1-sub_name': 'smile',
        'form-1-is_completed': 'False',
        }

        response = self.client.post(reverse('view-task', args=[str(test_board.id), str(test_task.id)]), {**task_form_data, **subtask_formset_data}, follow=True)
        # form validation failing?*
        self.assertRedirects(response, reverse('index'))

    def test_invalid_form_errors(self):  
        pass 

# new task -> url, template, logged in, not logged in, validation
class NewTaskViewTest(TestCase):
    def setUp(self):
        test_user1 = User.objects.create_user(username='testuser1', password='1X<ISRUkw+tuK')
        test_user1.save()
        
        # create board
        test_board = Board.objects.create(name='platform launch', user=test_user1)

        # two columns for this board
        test_column_1 = Column.objects.create(col_name='todo', board=test_board)

    def test_newtaskview_redirect_if_user_not_logged_in(self):
        test_board = Board.objects.get(name='platform launch')
        response = self.client.get(reverse('new-task', args=[str(test_board.id)]))
        self.assertRedirects(response, f'/taskmanager/accounts/login?next=/taskmanager/board/{test_board.id}/new-task')

    def test_newtaskview_url_exists(self):
        login = self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        test_board = Board.objects.get(name='platform launch')
        response = self.client.get(f'/taskmanager/board/{test_board.id}/new-task')
        self.assertEqual(response.status_code, 200)

    def test_newtaskview__uses_correct_template(self):
        login = self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        test_board = Board.objects.get(name='platform launch')
        response = self.client.get(reverse('new-task', args=[str(test_board.id)]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'components/forms/task_form.html')


    def test_newtaskview_initial_forms(self):
        login = self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        test_board = Board.objects.get(name='platform launch')
        response = self.client.get(reverse('new-task', args=[str(test_board.id)]))

        self.assertEqual(response.status_code, 200)
        self.assertTrue('task_form' in response.context)
        self.assertTrue('subtask_formset' in response.context)
        # empty formset
        self.assertEqual(len(response.context['subtask_formset']), 0)
        # columns options*

    # post
    def test_valid_newtaskview_form_redirects_to_boarddetail(self):
        login = self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        test_board = Board.objects.get(name='platform launch')
        test_column = Column.objects.get(col_name='todo')
        task_form_data = { 'title': 'Brainstorm', 'description': '', 'column': test_column.id }
        subtask_formset_data = {
        'form-INITIAL_FORMS': '0',
        'form-TOTAL_FORMS': '1',
        'form-MAX_NUM_FORMS': '',
        'form-0-sub_name': 'make coffee',
        }

        response = self.client.post(reverse('new-task', args=[str(test_board.id)]), {**task_form_data, **subtask_formset_data}, follow=True)
        self.assertRedirects(response, reverse('board-detail', args=[str(test_board.id)]))


    def test_invalid_newtaskview_form_errors(self):
        login = self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        test_board = Board.objects.get(name='platform launch')
        test_column = Column.objects.get(col_name='todo')
        # empty title
        task_form_data = { 'title': '', 'description': '', 'column': test_column.id }
        # empty sub_name
        subtask_formset_data = {
        'form-INITIAL_FORMS': '0',
        'form-TOTAL_FORMS': '1',
        'form-MAX_NUM_FORMS': '',
        'form-0-sub_name': '',
        }

        response = self.client.post(reverse('new-task', args=[str(test_board.id)]), {**task_form_data, **subtask_formset_data}, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response.context['task_form'], 'title', 'Can\'t be empty')
        self.assertFormError(response.context['subtask_formset'][0], 'sub_name', 'Can\'t be empty')
       

# edit task -> url, template, logged in, not logged in, validation
class EditTaskViewTest(TestCase):
    def setUp(self):
        test_user1 = User.objects.create_user(username='testuser1', password='1X<ISRUkw+tuK')
        test_user1.save()
        
        # create board
        test_board = Board.objects.create(name='platform launch', user=test_user1)

        # two columns for this board
        test_column_1 = Column.objects.create(col_name='todo', board=test_board)
        test_column_2 = Column.objects.create(col_name='done', board=test_board)

        # setup task
        test_task = Task.objects.create(title='brainstorm', description='30 min session', column=test_column_1)

        # two subtasks
        test_subtask_1 = SubTask.objects.create(sub_name='make coffee', is_completed='True', task=test_task)
        test_subtask_2 = SubTask.objects.create(sub_name='drink coffee', is_completed='False', task=test_task) 
       

    def test_redirect_if_user_not_logged_in(self):
        test_board = Board.objects.get(name='platform launch')
        test_task = Task.objects.get(title='brainstorm')
        response = self.client.get(reverse('edit-task', args=[str(test_board.id), str(test_task.id)]))
        self.assertRedirects(response, f'/taskmanager/accounts/login?next=/taskmanager/board/{test_board.id}/edit-task/{test_task.id}')

    def test_url_exists(self):
        login = self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        test_board = Board.objects.get(name='platform launch')
        test_task = Task.objects.get(title='brainstorm')
        response = self.client.get(f'/taskmanager/board/{test_board.id}/edit-task/{test_task.id}')
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        login = self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        test_board = Board.objects.get(name='platform launch')
        test_task = Task.objects.get(title='brainstorm')
        response = self.client.get(reverse('edit-task', args=[str(test_board.id), str(test_task.id)]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'components/forms/edit_task_form.html')

    def test_initial_form_values(self):
        login = self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        test_board = Board.objects.get(name='platform launch')
        test_column = Column.objects.get(col_name='todo')
        test_task = Task.objects.get(title='brainstorm')
        response = self.client.get(reverse('edit-task', args=[str(test_board.id), str(test_task.id)]))

        self.assertTrue('task_form' in response.context)
        self.assertTrue('subtask_formset' in response.context)
        # task form initial values
        self.assertEqual(response.context['task_form'].initial['column'], test_column.id)
        # subtask formset len & initial values
        self.assertEqual(len(response.context['subtask_formset']), 2)
        self.assertEqual(response.context['subtask_formset'][0].initial['sub_name'], 'drink coffee')
        self.assertEqual(response.context['subtask_formset'][1].initial['sub_name'], 'make coffee')
        

    # post
    def test_valid_form_redirects_to_index(self):
        login = self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        test_board = Board.objects.get(name='platform launch')
        test_column = Column.objects.get(col_name='todo')
        test_task = Task.objects.get(title='brainstorm')

        task_form_data = { 'title': 'brainstorm', 'description': '', 'column': test_column.id }

        subtask_formset_data = {
         'form-INITIAL_FORMS': '0',
         'form-TOTAL_FORMS': '1',
         'form-MAX_NUM_FORMS': '',
         'form-0-sub_name': '10 min session',      
        }

        response = self.client.post(reverse('edit-task', args=[str(test_board.id), str(test_task.id)]), {**task_form_data, **subtask_formset_data}, follow=True)
        self.assertRedirects(response, reverse('board-detail', args=[str(test_board.id)]))
        

    def test_invalid_form_errors(self):  
        login = self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        test_board = Board.objects.get(name='platform launch')
        # test_column = Column.objects.get(col_name='todo')
        test_task = Task.objects.get(title='brainstorm')

        task_form_data = { 'title': '', 'description': '30 min session', 'column': '' }

        subtask_formset_data = {
         'form-INITIAL_FORMS': '0',
         'form-TOTAL_FORMS': '1',
         'form-MAX_NUM_FORMS': '',
         'form-0-sub_name': '',      
        }

        response = self.client.post(reverse('edit-task', args=[str(test_board.id), str(test_task.id)]), {**task_form_data, **subtask_formset_data})
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response.context['task_form'], 'title', 'Can\'t be empty')
        self.assertFormError(response.context['task_form'], 'column', 'You need to select a column')
        self.assertFormError(response.context['subtask_formset'][0], 'sub_name', 'Can\'t be empty')
        


# delete task -> url, template, logged in, not logged in
class DeleteTaskViewTest(TestCase):
    def setUp(self):
        test_user1 = User.objects.create_user(username='testuser1', password='1X<ISRUkw+tuK')
        test_user1.save()
        
        # create board
        test_board = Board.objects.create(name='platform launch', user=test_user1)

        # two columns for this board
        test_column_1 = Column.objects.create(col_name='todo', board=test_board)

        # setup task
        test_task = Task.objects.create(title='brainstorm', description='30 min session', column=test_column_1)

        # two subtasks
        test_subtask_1 = SubTask.objects.create(sub_name='make coffee', is_completed='True', task=test_task)
        test_subtask_2 = SubTask.objects.create(sub_name='drink coffee', is_completed='False', task=test_task)

    def test_redirect_if_user_not_logged_in(self):
        test_task = Task.objects.get(title='brainstorm')
        response = self.client.get(reverse('delete-task', args=[str(test_task.id)]))
        self.assertRedirects(response, f'/taskmanager/accounts/login?next=/taskmanager/board/{test_task.id}/delete-task')

    def test_url_exists(self):
        login = self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        test_task = Task.objects.get(title='brainstorm')
        response = self.client.get(f'/taskmanager/board/{test_task.id}/delete-task')
        self.assertEqual(response.status_code, 200)
      
    def test_view_uses_correct_template(self):
        login = self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        test_task = Task.objects.get(title='brainstorm')
        response = self.client.get(reverse('delete-task', args=[str(test_task.id)]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'components/forms/delete_task_form.html')

    def test_success_redirects_to_index(self):
        login = self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        test_task = Task.objects.get(title='brainstorm')
        response = self.client.post(reverse('delete-task', args=[str(test_task.id)]), {}, follow=True)
        self.assertRedirects(response, reverse('index'))


# subtask form -> url, template, logged in, not logged in, validation
class SubtaskFormViewTest(TestCase):
    def setUp(self):
        test_user1 = User.objects.create_user(username='testuser1', password='1X<ISRUkw+tuK')
        test_user1.save()

    def test_redirect_if_user_not_logged_in(self):
        response = self.client.get(reverse('add-subtask', args=[str(1)]))
        self.assertRedirects(response, '/taskmanager/accounts/login?next=/taskmanager/board/subtask/1')

    def test_url_exists(self):
        login = self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        response = self.client.get('/taskmanager/board/subtask/1') 
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        login = self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        response = self.client.get(reverse('add-subtask', args=[str(1)]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'components/forms/subtask_form.html')  

    def test_number_of_formsets(self):
        login = self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        response = self.client.get(reverse('add-subtask', args=[str(3)]))

        self.assertEqual(response.status_code, 200)
        self.assertTrue('new_formset' in response.context)
        self.assertTrue('new_total_formsets' in response.context)
        # new formset total
        self.assertEqual(response.context['new_total_formsets'], 4)

