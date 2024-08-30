from django.test import TestCase

from taskmanager.auth_forms import LoginForm

# login form -> username, password
class LoginFormTest(TestCase):
    def test_login_form_fields(self):
        form = LoginForm()
        self.assertIn('username', form.fields)
        self.assertIn('password', form.fields)
    
    def test_username_required(self):
        form = LoginForm(data={'username': '', 'password': '1X<ISRUkw+tuK'})
        errors_name = form['username'].errors.as_data()
        self.assertEqual(len(errors_name), 1)
        self.assertEqual(errors_name[0].code, 'required')
        self.assertFalse(form.is_valid())

    def test_password_required(self):
        form = LoginForm(data={'username': 'testuser1', 'password': ''})
        errors_password = form['password'].errors.as_data()
        self.assertEqual(len(errors_password), 1)
        self.assertEqual(errors_password[0].code, 'required')
        self.assertFalse(form.is_valid())   