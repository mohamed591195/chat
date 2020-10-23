from django.test import TestCase
from accounts.models import User


class TestUserModel(TestCase):

    def test_create_user(self):

        user = User.objects.create_user(
            email='basic_user@domain.com', password='56711'
        )

        self.assertEqual(user.email, 'basic_user@domain.com')

        self.assertTrue(user.check_password('56711'))

        self.assertTrue(user.is_active)

        self.assertFalse(user.is_superuser)
        self.assertFalse(user.is_staff)

        with self.assertRaises(TypeError):
            User.objects.create_user()

        with self.assertRaises(ValueError):
            User.objects.create_user(email='', password='')

        try:
            user.username
        except AttributeError:
            pass

    def test_create_superuser(self):

        superuser = User.objects.create_superuser(
            email='superuser@domain.com', password='202020')

        self.assertEqual(superuser.email, 'superuser@domain.com')

        self.assertTrue(superuser.check_password('202020'))

        self.assertTrue(superuser.is_active)

        self.assertTrue(superuser.is_superuser)
        self.assertTrue(superuser.is_staff)

        with self.assertRaises(ValueError):
            User.objects.create_superuser(
                email='superuser2@domain.com', password='202020', is_staff=False)

        with self.assertRaises(ValueError):
            User.objects.create_superuser(
                email='superuser2@domain.com', password='202020', is_superuser=False)
