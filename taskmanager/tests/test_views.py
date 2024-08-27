from django.test import TestCase, Client
from django.urls import reverse
from taskmanager.models import Board
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

    def test_redirect_if_not_logged_in(self):
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

    def test_redirect_if_not_logged_in(self):
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

    def test_invalid_formset(self):
        login = self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        board_form_data = {'name': 'platform launch'}
        formset_data = {
        # management_form data
        'form-INITIAL_FORMS': '0',
        'form-TOTAL_FORMS': '1',
        'form-MAX_NUM_FORMS': '',
        # empty col_name
        'form-0-col_name': '',
        }

        response = self.client.post(reverse('new-board'), {**board_form_data, **formset_data})
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response.context['formset'][0], 'col_name', 'Can\'t be empty')  

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

# column form -> url, template, logged in, not logged in, validation

# delete board -> url, template, logged in, not logged in

# task view -> url, template, logged in, not logged in, validation

# new task -> url, template, logged in, not logged in, validation

# edit task -> url, template, logged in, not logged in, validation

# delete task -> url, template, logged in, not logged in

# subtask form -> url, template, logged in, not logged in, validation

