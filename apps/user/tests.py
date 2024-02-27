import re
from datetime import datetime
from typing import Optional

from django.test import TestCase
from apps.user.models import User
from rest_framework.test import APIClient
from rest_framework import status


class ListAllUsersGenericViewTest(TestCase):
    datetime_regex = re.compile(r'\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d+Z')

    def setUp(self):
        # Создаем тестовых пользователей
        self.user = User.objects.create_user(
            email='test.email@mail.ru',
            first_name='test',
            last_name='user',
            username='testUser',
            password='password',
        )
        self.user = User.objects.create_user(
            email='test1.email@mail.ru',
            first_name='test1',
            last_name='user1',
            username='testUser1',
            password='password1',
        )
        self.admin = User.objects.create_superuser(
            email='test.admin@mail.ru',
            first_name='admintest',
            last_name='testadmin',
            username='admin',
            password='admin',
            is_staff=True,
        )

        self.client = APIClient()

    def test_get_users_as_admin(self):
        # Администратор получает список пользователей
        self.client.force_authenticate(user=self.admin)
        response = self.client.get('http://127.0.0.1:8000/api/v1/users/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), User.objects.count() - 1)
        self.assertIsInstance(response.data, list)

        for user in response.data:
            self.assertIsInstance(user['email'], str)
            self.assertIsInstance(user['first_name'], str)
            self.assertIsInstance(user['last_name'], str)
            self.assertIsInstance(user['username'], str)
            self.assertIsInstance(user['phone'], (Optional[str]))    # тут изменила из str | None
            self.assertIsInstance(user['is_staff'], bool)
            self.assertIsInstance(user['is_superuser'], bool)
            self.assertIsInstance(user['is_verified'], bool)
            self.assertIsInstance(user['is_active'], bool)
            self.assertTrue(self.datetime_regex.match(user['date_joined']), datetime)
            self.assertTrue(self.datetime_regex.match(user['last_login']), datetime)

    def test_get_users_as_non_admin(self):
        # Неадминистратор получает запрет доступа
        self.client.force_authenticate(user=self.user)
        response = self.client.get('http://127.0.0.1:8000/api/v1/users/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_no_users(self):
        # Проверка на отсутствие пользователей
        User.objects.all().delete()
        self.client.force_authenticate(user=self.admin)
        response = self.client.get('http://127.0.0.1:8000/api/v1/users/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
