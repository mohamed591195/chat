from django.test import TestCase
from accounts.forms import UserRegisterationForm


class TestAccountsForms(TestCase):

    def test_registeration_form(self):

        # valid data
        data = {
            'first_name': 'Mohammad',
            'last_name': 'samir',
            'email': 'mohamedsamir591195@gmail.com',
            'password1': '*8#Momomomom',
            'password2': '*8#Momomomom'
        }

        form = UserRegisterationForm(data=data)

        self.assertTrue(form.is_valid())

        # unvalid email
        # 1
        data['email'] = 'mohamedsamir591195@gmail'

        form = UserRegisterationForm(data=data)

        self.assertIn('email', form.errors)

        # 2
        data['email'] = ''

        form = UserRegisterationForm(data=data)

        self.assertIn('email', form.errors)

        # first & last names unrequired
        data.update({
            'first_name': '',
            'last_name': '',
            'email': 'mohamedsamir591195@gmail.com'
        })

        form = UserRegisterationForm(data=data)

        self.assertTrue(form.is_valid())
