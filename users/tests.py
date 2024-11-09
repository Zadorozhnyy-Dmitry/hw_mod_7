from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status

from lms.models import Course
from users.models import User, Subs


class SubsTestCase(APITestCase):
    """Тесты для подписок"""

    def setUp(self):
        """Фикстуры"""
        self.user = User.objects.create(email='admin@sky.pro')
        self.course = Course.objects.create(name='Python', description='топ язык', owner=self.user)
        self.subs = Subs.objects.create(user=self.user, course=self.course)
        self.client.force_authenticate(user=self.user)

    def test_subs_create(self):
        """Тестирование подписки и отписки"""
        # Отписка
        url = reverse('users:subs-create')
        data = {
            'course': self.course.pk
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'Вы отписались')

        # Подписка
        url = reverse('users:subs-create')
        data = {
            'course': self.course.pk
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'Вы подписались')
        self.assertTrue(Subs.objects.filter(user=self.user, course=self.course).exists())

    def test_subs_list(self):
        """Тестирование вывода списка подписок"""
        url = reverse('users:subs-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['course'], self.course.id)
