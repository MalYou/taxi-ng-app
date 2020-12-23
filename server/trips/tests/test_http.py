import base64
import json

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from trips.models import Trip


AUTHENTICATION_URL = reverse('sign_up')
LOGIN_URL = reverse('log_in')
TRIPS_URL = reverse('trip:trip_list')
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


class HttpTripTest(TestCase):
    """Test trip endpoint"""

    def setUp(self):
        self.client = APIClient()
        user = sample_user()

        res = self.client.post(LOGIN_URL, {
            'username': user.username,
            'password': PASSWORD,
        })

        self.access = res.data['access']

    def test_user_can_list_trips(self):
        """Test that connected user can retriev trips"""
        trips = [
            Trip.objects.create(pick_up_address='A', drop_off_address='B'),
            Trip.objects.create(pick_up_address='B', drop_off_address='C'),
        ]

        res = self.client.get(
            TRIPS_URL, HTTP_AUTHORIZATION=f'Bearer {self.access}'
        )

        exp_ids = [str(trip.id) for trip in trips]
        res_ids = [trip.get('id') for trip in res.data]

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertCountEqual(exp_ids, res_ids)

    def test_user_can_retrieve_trip_by_id(self):
        """Test that the authenticated user can get trip detail"""
        trip = Trip.objects.create(
            pick_up_address='A',
            drop_off_address='B',
            status='REQUEST'
        )

        res = self.client.get(trip.get_absolute_url(),
                              HTTP_AUTHORIZATION=f'Bearer {self.access}')

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(str(trip.id), res.data['id'])
