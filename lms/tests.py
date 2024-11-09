from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status

from lms.models import Course, Lesson
from users.models import User


class CourseTestCase(APITestCase):
    """Тесты для курсов"""

    def setUp(self):
        """Фикстуры"""
        self.user = User.objects.create(email='admin@sky.pro')
        self.course = Course.objects.create(name='Python', description='топ язык', owner=self.user)
        self.lesson = Lesson.objects.create(name='Урок 1', course=self.course, video_url='https://youtube.com/123',
                                            owner=self.user)
        self.client.force_authenticate(user=self.user)

    def test_course_retrieve(self):
        """Тестирование вывода одного курса"""
        url = reverse('lms:course-detail', args=(self.course.pk,))
        response = self.client.get(url)
        data = response.json()
        self.assertEqual(
            response.status_code, status.HTTP_200_OK
        )
        self.assertEqual(
            data.get('name'), self.course.name
        )

    def test_course_create(self):
        """Тестирование создания курса"""
        url = reverse('lms:course-list')
        data = {
            'name': 'C++'
        }
        response = self.client.post(url, data)
        self.assertEqual(
            response.status_code, status.HTTP_201_CREATED
        )
        self.assertEqual(
            Course.objects.all().count(), 2
        )

    def test_course_update(self):
        """Тестирование изменения одного курса"""
        url = reverse('lms:course-detail', args=(self.course.pk,))
        data = {
            'name': 'Java'
        }
        response = self.client.patch(url, data)
        data = response.json()
        self.assertEqual(
            response.status_code, status.HTTP_200_OK
        )
        self.assertEqual(
            data.get('name'), 'Java'
        )

    def test_course_delete(self):
        """Тестирование удаления одного курса"""
        url = reverse('lms:course-detail', args=(self.course.pk,))
        response = self.client.delete(url)
        self.assertEqual(
            response.status_code, status.HTTP_204_NO_CONTENT
        )
        self.assertEqual(
            Course.objects.all().count(), 0
        )

    def test_course_list(self):
        """Тестирование вывода всех курсов"""
        url = reverse('lms:course-list')
        response = self.client.get(url)
        data = response.json()
        result = {
            "count": 1,
            "next": None,
            "previous": None,
            "results": [
                {
                    "id": self.course.pk,
                    "is_subs": False,
                    "name": self.course.name,
                    "description": self.course.description,
                    "preview": None,
                    "owner": self.user.pk
                }
            ]
        }

        self.assertEqual(
            response.status_code, status.HTTP_200_OK
        )
        self.assertEqual(
            data, result
        )


class LessonTestCase(APITestCase):
    """Тесты для уроков"""

    def setUp(self):
        """Фикстуры"""
        self.user = User.objects.create(email='admin@sky.pro')
        self.course = Course.objects.create(name='Python', description='топ язык', owner=self.user)
        self.lesson = Lesson.objects.create(name='Урок 1', course=self.course, video_url='https://youtube.com/123',
                                            owner=self.user)
        self.client.force_authenticate(user=self.user)

    def test_lesson_retrieve(self):
        """Тестирование вывода одного урока"""
        url = reverse('lms:lessons-retrieve', args=(self.lesson.pk,))
        response = self.client.get(url)
        data = response.json()
        self.assertEqual(
            response.status_code, status.HTTP_200_OK
        )
        self.assertEqual(
            data.get('name'), self.lesson.name
        )

    def test_lesson_create(self):
        """Тестирование создания урока"""
        url = reverse('lms:lessons-create')
        data = {
            'name': 'lesson_test',
            'video_url': 'https://youtube.com/321'
        }
        response = self.client.post(url, data)
        self.assertEqual(
            response.status_code, status.HTTP_201_CREATED
        )
        self.assertEqual(
            Lesson.objects.all().count(), 2
        )

    def test_lesson_update(self):
        """Тестирование изменения одного урока"""
        url = reverse('lms:lessons-update', args=(self.lesson.pk,))
        data = {
            'name': 'Урок тест2'
        }
        response = self.client.patch(url, data)
        data = response.json()
        self.assertEqual(
            response.status_code, status.HTTP_200_OK
        )
        self.assertEqual(
            data.get('name'), 'Урок тест2'
        )

    def test_lesson_delete(self):
        """Тестирование удаления одного урока"""
        url = reverse('lms:lessons-delete', args=(self.lesson.pk,))
        response = self.client.delete(url)
        self.assertEqual(
            response.status_code, status.HTTP_204_NO_CONTENT
        )
        self.assertEqual(
            Lesson.objects.all().count(), 0
        )

    def test_lesson_list(self):
        """Тестирование вывода всех уроков"""
        url = reverse('lms:lessons-list')
        response = self.client.get(url)
        data = response.json()
        result = {
            "count": 1,
            "next": None,
            "previous": None,
            "results": [
                {
                    "id": self.lesson.pk,
                    "video_url": self.lesson.video_url,
                    "name": self.lesson.name,
                    "preview": None,
                    "course": self.course.pk,
                    "owner": self.user.pk
                }
            ]
        }
        self.assertEqual(
            response.status_code, status.HTTP_200_OK
        )
        self.assertEqual(
            data, result
        )
