from rest_framework.test import APITestCase
from rest_framework import status


class RegistrationTestCase(APITestCase):
    def test_success_registration(self):
        data = {
            'email': 'test@example.com',
            'username': 'test',
            'password': 'mypass1234'
        }
        response = self.client.post('/register/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_invalid_registration(self):
        data = {
            'email': 'test example.com',
            'username': 'test',
            'password': 'mypass12'
        }
        response = self.client.post('/register/', data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
