from django.test import TestCase
from django.urls import reverse
from accounts.models import User
from django.contrib.auth import get_user


class TestAccountsViews(TestCase):

    def test_user_registeration_view(self):

        # get request
        response = self.client.get(reverse('register_view'))

        self.assertEqual(response.status_code, 200)

        self.assertTemplateUsed(response, 'accounts/register.html')

        # post request

        data = {
            'first_name': 'Mohammad',
            'last_name': 'samir',
            'email': 'mohamedsamir591195@gmail.com',
            'password1': 'testing4321*',
            'password2': 'testing4321*'
        }

        # 1 valid data
        response = self.client.post(
            reverse('register_view'),
            data=data
        )

        self.assertEqual(response.status_code, 302)

        self.assertTrue(
            User.objects.filter(email='mohamedsamir591195@gmail.com').exists()
        )

        # checking authentication after registeration
        # get user need an http request session, test client object also has session attr
        user = get_user(self.client)
        self.assertTrue(user.is_authenticated)

        # 2 repeated email address
        response = self.client.post(
            reverse('register_view'),
            data=data
        )

        self.assertContains(response, 'User with this Email already exists')
        # errors related to password are handled from django code
