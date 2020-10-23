from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model, get_user

User = get_user_model()

class TestConversations(TestCase):

    def setUp(self):

        User.objects.create_user(email='test_email@mail.com', password='testing4321*')

    def test_home_view_get_request(self):
        
        # not authenticated user 
        response = self.client.get(reverse('home_view'))
        
        self.assertRedirects(response, reverse('login_view') + '?next=/')

        self.client.login(email='test_email@mail.com', password='testing4321*')

        user = get_user(self.client)
        self.assertTrue(user.is_authenticated)
        
        # authenticated 
        response = self.client.get(reverse('home_view'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'conversations/home.html')
