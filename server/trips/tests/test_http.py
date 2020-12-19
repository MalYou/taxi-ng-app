import base64
import json

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient


AUTHENTICATION_URL = reverse('sign_up')
LOGIN_URL = reverse('log_in')
PASSWORD = 'Test1245'


def sample_user(email='user@gmail.com', password=PASSWORD):
    """Create a sample user for tests"""
    return get_user_model().objects.create_user(
        username='Test',
        email=email,
        password=password,
    )


class AuthenticationTest(TestCase):
    """Test that a new user can signup"""

    def setUp(self):
        self.client = APIClient()

    def test_user_can_sign_up(self):
        """Test that a new user can signup"""
        payload = {
            'username': 'Test',
            'email': 'test@gmail.com',
            'password1': PASSWORD,
            'password2': PASSWORD
        }

        res = self.client.post(AUTHENTICATION_URL, payload)

        user = get_user_model().objects.last()

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(user.username, payload['username'])
        self.assertEqual(user.email, payload['email'])
        self.assertTrue(user.check_password(payload['password1']))

    def test_user_can_login(self):
        """Test that a user can login with valid credentials"""
        user = sample_user()
        payload = {
            'username': user.username,
            'password': PASSWORD
        }

        res = self.client.post(LOGIN_URL, payload)

        # Parse payload for access token
        access = res.data['access']
        hearder, token_payload, signature = access.split('.')
        decoded_token_payload = base64.b64decode(f'{token_payload}==')
        payload_data = json.loads(decoded_token_payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIsNotNone(res.data['refresh'])
        self.assertEqual(payload_data['user_id'], user.id)
        self.assertEqual(payload_data['email'], user.email)
        self.assertEqual(payload_data['username'], user.username)
