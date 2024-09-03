
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model

User = get_user_model()

class UserManagementTests(APITestCase):

    def setUp(self):
        self.admin_user = User.objects.create_user(username='adminuser', password='adminpass', role='admin')
        self.customer_user = User.objects.create_user(username='customeruser', password='customerpass', role='customer')
        self.admin_token = self.client.post(reverse('login'), {'username': 'adminuser', 'password': 'adminpass'}).response_data['access']
        self.customer_token = self.client.post(reverse('login'), {'username': 'customeruser', 'password': 'customerpass'}).response_data['access']

    def test_register_user(self):
        data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password': 'newpassword123',
            'role': 'customer'
        }
        response = self.client.post(reverse('register'), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_login_user(self):
        data = {'username': 'adminuser', 'password': 'adminpass'}
        response = self.client.post(reverse('login'), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)

    def test_access_customer_dashboard_with_customer_role(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.customer_token)
        response = self.client.get(reverse('customer-home'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_access_admin_dashboard_with_customer_role(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.customer_token)
        response = self.client.get(reverse('admin-home'))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_access_admin_dashboard_with_admin_role(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.admin_token)
        response = self.client.get(reverse('admin-home'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_access_customer_dashboard_with_admin_role(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.admin_token)
        response = self.client.get(reverse('customer-home'))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
