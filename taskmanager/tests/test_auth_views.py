from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User


class SignUpViewTest(TestCase):
        
    def test_url_exists(self):
        response = self.client.get('/taskmanager/accounts/sign-up')
        self.assertEqual(response.status_code, 200)

    def test_url_accessible_by_name(self):
        response = self.client.get(reverse('sign-up'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('sign-up'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/signup.html')

    def test_view_context_has_form_with_correct_fields(self):
        response = self.client.get(reverse('sign-up'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue('form' in response.context)
        # form fields
        form = response.context['form']
        self.assertIn('username', form.fields)
        self.assertIn('password1', form.fields)
        self.assertIn('password2', form.fields)

    # post
    def test_required_fields(self):
        form_data = {'username': '', 'password1': '', 'password2': ''}
        response = self.client.post(reverse('sign-up'), form_data)
        self.assertEqual(response.status_code, 200)
        # errors
        self.assertFormError(response.context['form'], 'username', 'This field is required.')
        self.assertFormError(response.context['form'], 'password1', 'This field is required.')
        self.assertFormError(response.context['form'], 'password2', 'This field is required.')

    def test_passwords_do_not_match_error(self):    
        form_data = {'username': 'testuser1', 'password1': '1X<ISRUkw+tuK', 'password2': '1X<ISRUkw+tu'}
        response = self.client.post(reverse('sign-up'), form_data)
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response.context['form'], 'password2', 'The two password fields didn’t match.')

    def test_password_required_length_error(self):    
        form_data = {'username': 'testuser1', 'password1': '1X<ISR', 'password2': '1X<ISR'}
        response = self.client.post(reverse('sign-up'), form_data)
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response.context['form'], 'password2', 'This password is too short. It must contain at least 8 characters.')

    def test_password_is_too_weak(self):    
        form_data = {'username': 'testuser1', 'password1': 'hello1234', 'password2': 'hello1234'}
        response = self.client.post(reverse('sign-up'), form_data)
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response.context['form'], 'password2', 'This password is too common.')

    def test_valid_signup_form_redirects_to_index(self):
        form_data = {'username': 'testuser1', 'password1': '1X<ISRUkw+tuK', 'password2': '1X<ISRUkw+tuK'}
        response = self.client.post(reverse('sign-up'), form_data, follow=True)
        self.assertRedirects(response, reverse('index'))

    def test_valid_signup_logs_the_user_in(self):
        form_data = {'username': 'testuser1', 'password1': '1X<ISRUkw+tuK', 'password2': '1X<ISRUkw+tuK'}
        response = self.client.post(reverse('sign-up'), form_data, follow=True)
        self.assertTrue(response.context['user'].is_active)    


class LoginViewTest(TestCase):
    def setUp(self):
        test_user1 = User.objects.create_user(username='testuser1', password='1X<ISRUkw+tuK')
        test_user1.save()

    def test_url_exists(self):
        response = self.client.get('/taskmanager/accounts/login')
        self.assertEqual(response.status_code, 200)

    def test_url_accessible_by_name(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/login.html')    
    
    def test_view_context_has_form(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue('form' in response.context)

    # post
    def test_incorrect_password_does_not_log_user_in(self):
        # form with incorrect password
        form_data = {'username': 'testuser1', 'password': '1X<ISRUkw+tu'}
        response = self.client.post(reverse('login'), form_data)
        self.assertEqual(response.status_code, 200)

    def test_valid_credentials_logs_user_in_and_redirects_to_index(self):
        form_data = {'username': 'testuser1', 'password': '1X<ISRUkw+tuK'}
        response = self.client.post(reverse('login'), form_data, follow=True)
        self.assertTrue(response.context['user'].is_active)
        self.assertRedirects(response, reverse('index'))


class LogoutViewTest(TestCase):
    def setUp(self):
        test_user1 = User.objects.create_user(username='testuser1', password='1X<ISRUkw+tuK')
        test_user1.save()

    def test_url_exists(self):
        response = self.client.get('/taskmanager/accounts/logout')
        self.assertEqual(response.status_code, 200)

    def test_url_accessible_by_name(self):
        response = self.client.get(reverse('logout'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('logout'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/logout.html')

    def test_logout_redirects_to_index(self):
        login = self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        response = self.client.post(reverse('logout'))
        self.assertRedirects(response, reverse('index'))        


        
