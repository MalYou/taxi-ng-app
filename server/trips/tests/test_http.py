from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient


AUTHENTICATION_URL = reverse('sign_up')


class AuthenticationTest(TestCase):
    """Test that a new user can signup"""

    def setUp(self):
        self.client = APIClient()

    def test_user_can_sign_up(self):
        """Test that a new user can signup"""
        payload = {
            'username': 'Test',
            'email': 'test@gmail.com',
            'password1': 'test145',
            'password2': 'test145'
        }

        res = self.client.post(AUTHENTICATION_URL, payload)

        user = get_user_model().objects.last()

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(user.username, payload['username'])
        self.assertEqual(user.email, payload['email'])
        self.assertTrue(user.check_password(payload['password1']))
