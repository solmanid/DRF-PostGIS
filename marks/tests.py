from django.contrib.gis.geos import Point
from rest_framework.test import APITestCase, APIClient

from accountants.models import Accountant
from accounts.models import User, OtpCode

from django.utils.timezone import now
from django.urls import reverse
from model_bakery import baker
from supervisors.models import Supervisor
from marks.models import PlacePoints, AcceptedPlace


class ShowMarksTest(APITestCase):
    def setUp(self):
        self.user = baker.make(User, username='root', password='root')
        self.point = baker.make(PlacePoints, user=self.user, location=Point(233214, 312423))
        self.url = '/en/marks/'

    def test_show_marks(self):
        response = self.client.get(
            path=self.url,
        )

        self.assertEqual(response.status_code, 200)


class MarksAddMarkTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='root',
            password='root',
            email='root@gmail.com'
        )
        # self.point = baker.make(PlacePoints, user=self.user, location=Point(233214, 312423))
        self.url = '/en/marks/add/'
        self.login = self.client.post('/en/accounts/login/', {'username': 'root', 'password': 'root'})
        code = OtpCode.objects.first()
        self.ver = self.client.post('/en/accounts/login/verify/', {'code': code.code})
        self.token = self.ver.data['token']

    def test_add_mark_with_auth(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')
        data = {
            'lat': 35323,
            'lng': 54221,
            'description': 'ok'
        }

        response = self.client.post(
            path=self.url,
            data=data
        )
        point = PlacePoints.objects.first()

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['description'], 'ok')

    def test_add_mark_no_auth(self):
        data = {
            'lat': 35323,
            'lng': 54221,
            'description': 'ok'
        }

        response = self.client.post(
            path=self.url,
            data=data
        )

        self.assertEqual(response.status_code, 401)

    def test_add_mark_invalid_data(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')
        data = {
            'lat': 'hi',
            'lng': 54221,
            'description': 'ok'
        }

        response = self.client.post(
            path=self.url,
            data=data
        )

        self.assertRaisesRegex(ValueError, 'could not convert string to float: ')
        self.assertEqual(response.status_code, 400)
