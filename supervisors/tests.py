import random

from django.contrib.gis.geos import Point
from rest_framework.test import APITestCase, APIClient

from accountants.models import Accountant
from accounts.models import User, OtpCode

from django.utils.timezone import now
from django.urls import reverse
from model_bakery import baker
from supervisors.models import Supervisor
from marks.models import PlacePoints, AcceptedPlace
from accountants.models import PaymentMark


class SupervisorProfileTest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.sup = Supervisor.objects.create_user(
            username='sup',
            password='root',
            email='sup@gmail.com',
            national_id='43433243',
            supervisor_code='34443235',
            supervisor_license='klenfk/fkvmv/vlfmvk',
            is_accountant=False,
            is_supervisor=True,
            is_people=False,
            user_type=User.Types.supervisor,
            last_login=now()
        )
        self.user = User.objects.create_user(
            username='root',
            password='root',
            email='root@gmail.com'
        )
        self.login = self.client.post('/en/accounts/login/', {'username': 'sup', 'password': 'root'})
        self.token = self.login.data['Token']
        self.login_user = self.client.post('/en/accounts/login/', {'username': 'root', 'password': 'root'})
        code = OtpCode.objects.first()
        self.ver = self.client.post('/en/accounts/login/verify/', {'code': code.code})
        self.token_user = self.ver.data['token']
        self.arg = self.sup.id
        self.url = reverse('supervisor_profile', args=[self.arg])

    def test_supervisor_profile_url(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')
        response = self.client.get(
            path=self.url,
        )
        self.assertEqual(response.status_code, 200)

    def test_supervisor_profile_response_data(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')
        response = self.client.get(
            path=self.url,
        )

        self.assertEqual(response.data['username'], 'sup')

    def test_supervisor_profile_invalid_user_type(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token_user}')
        response = self.client.get(
            path=self.url,
        )
        self.assertEqual(response.status_code, 403)


class SupervisorShowMarksTest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.sup = Supervisor.objects.create_user(
            username='sup',
            password='root',
            email='sup@gmail.com',
            national_id='43433243',
            supervisor_code='34443235',
            supervisor_license='klenfk/fkvmv/vlfmvk',
            is_accountant=False,
            is_supervisor=True,
            is_people=False,
            user_type=User.Types.supervisor,
            last_login=now()
        )
        self.user = User.objects.create_user(
            username='root',
            password='root',
            email='root@gmail.com'
        )
        self.login = self.client.post('/en/accounts/login/', {'username': 'sup', 'password': 'root'})
        self.token = self.login.data['Token']
        self.login_user = self.client.post('/en/accounts/login/',
                                           {'username': 'root', 'password': 'root'})
        code = OtpCode.objects.first()
        self.ver = self.client.post('/en/accounts/login/verify/', {'code': code.code})
        self.token_user = self.ver.data['token']
        self.url = reverse('mark_for_supervisor')
        self.point = baker.make(PlacePoints, user=self.user, _quantity=5, location=Point(233214, 312423))

    def test_show_marks_correctly(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')
        response = self.client.get(
            path=self.url,
        )
        self.assertEqual(response.status_code, 200)

    def test_show_to_only_supervisor(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token_user}')
        response = self.client.get(
            path=self.url,
        )
        self.assertEqual(response.status_code, 403)


class SupervisorAcceptTest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.sup = Supervisor.objects.create_user(
            username='sup',
            password='root',
            email='sup@gmail.com',
            national_id='43433243',
            supervisor_code='34443235',
            supervisor_license='klenfk/fkvmv/vlfmvk',
            is_accountant=False,
            is_supervisor=True,
            is_people=False,
            user_type=User.Types.supervisor,
            last_login=now()
        )
        self.user = User.objects.create_user(
            username='root',
            password='root',
            email='root@gmail.com'
        )
        self.login = self.client.post('/en/accounts/login/', {'username': 'sup', 'password': 'root'})
        self.token = self.login.data['Token']
        self.login_user = self.client.post('/en/accounts/login/',
                                           {'username': 'root', 'password': 'root'})
        code = OtpCode.objects.first()
        self.ver = self.client.post('/en/accounts/login/verify/', {'code': code.code})
        self.token_user = self.ver.data['token']
        self.url = reverse('accept_mark')
        self.point = baker.make(PlacePoints, user=self.user, _quantity=5, location=Point(233214, 312423))
        self.accept_place = baker.make(AcceptedPlace, supervisor=self.sup, mark=self.point[0], level=AcceptedPlace.Levels.hard,
                                       action=AcceptedPlace.Status.accepted)

    def test_show_accepted_place_to_supervisor(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')
        response = self.client.get(
            path=self.url,
        )

        self.assertEqual(response.status_code, 200)

    def test_add_accept_place_by_supervisor(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')
        data = {
            'mark': self.point[1].id,
            'description': 'hi this is added by test',
            'action': '1',
            'level': '2'
        }
        response = self.client.post(
            path=self.url,
            data=data
        )
        self.assertEqual(response.status_code, 201)

    def test_add_accept_place_wrong_action(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')
        data = {
            'mark': self.point[1].id,
            'description': 'hi this is added by test',
            'action': '3',
            'level': '2'
        }

        response = self.client.post(
            path=self.url,
            data=data
        )
        self.assertEqual(response.status_code, 400)

    def test_add_accept_place_two_times(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')
        data = {
            'mark': self.point[0].id,
            'description': 'hi this is added by test',
            'action': '1',
            'level': '2'
        }

        response = self.client.post(
            path=self.url,
            data=data
        )
        self.assertEqual(response.status_code, 400)


