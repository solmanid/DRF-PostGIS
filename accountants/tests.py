from rest_framework.test import APITestCase, APIClient

from accountants.models import Accountant
from accounts.models import User, OtpCode

from django.utils.timezone import now
from django.urls import reverse
from model_bakery import baker
from supervisors.models import Supervisor
from marks.models import PlacePoints, AcceptedPlace


class AccountantProfileTest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.accountant = Accountant.objects.create_user(
            username='acc',
            password='root',
            email='accountant@gmail.com',
            national_id='43433243',
            accountant_code='34443235',
            accountant_license='klenfk/fkvmv/vlfmvk',
            is_accountant=True,
            is_supervisor=False,
            is_people=False,
            user_type=User.Types.accountant,
            last_login=now()
        )
        self.user = User.objects.create_user(
            username='root',
            password='root',
            email='root@gmail.com'
        )
        self.login = self.client.post('/en/accounts/login/', {'username': 'acc', 'password': 'root'})
        self.token = self.login.data['Token']
        self.login_user = self.client.post('/en/accounts/login/', {'username': 'root', 'password': 'root'})
        code = OtpCode.objects.first()
        self.ver = self.client.post('/en/accounts/login/verify/', {'code': code.code})
        self.token_user = self.ver.data['token']
        self.arg = self.accountant.id
        self.url = reverse('accountant_profile', args=[self.arg])

    def test_accountant_profile_url(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')
        response = self.client.get(
            path=self.url,
        )
        self.assertEqual(response.status_code, 200)

    def test_accountant_profile_response_data(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')
        response = self.client.get(
            path=self.url,
        )

        self.assertEqual(response.data['username'], 'acc')

    def test_accountant_profile_invalid_user_type(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token_user}')
        response = self.client.get(
            path=self.url,
        )

        self.assertEqual(response.status_code, 403)


class AccountantAcceptedMarkTest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = baker.make(User, username='root', password='root')
        self.supervisor = Supervisor.objects.create_user(
            username='sup',
            password='root',
            last_login=now(),
            email='sup@gmail.com',
            national_id='43433213',
            supervisor_code='34443835',
            is_accountant=False,
            is_supervisor=True,
            is_people=False,
            user_type=User.Types.supervisor,
            supervisor_license='klenfk/fkvmv/dws',

        )

        self.accountant = Accountant.objects.create_user(
            username='acc',
            password='root',
            email='accountant@gmail.com',
            national_id='43433243',
            accountant_code='34443235',
            accountant_license='klenfk/fkvmv/vlfmvk',
            is_accountant=True,
            is_supervisor=False,
            is_people=False,
            user_type=User.Types.accountant,
            last_login=now()
        )
        self.point = baker.make(PlacePoints, user=self.user)
        self.accept_place = baker.make(AcceptedPlace, supervisor=self.supervisor, mark=self.point)
        self.login = self.client.post('/en/accounts/login/', {'username': 'acc', 'password': 'root'})
        self.token = self.login.data['Token']

        self.login_sup = self.client.post('/en/accounts/login/', {'username': 'sup', 'password': 'root'})
        self.token_sup = self.login_sup.data['Token']
        self.url = reverse('accountant_mark')

    def test_show_list_of_accepted_place(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')
        response = self.client.get(
            path=self.url
        )
        self.assertEqual(response.status_code, 200)

    def test_does_not_show_list_for_users(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token_sup}')
        response = self.client.get(
            path=self.url
        )
        self.assertEqual(response.status_code, 403)


class AccountantAddPaymentTest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = baker.make(User, username='root', password='root')
        self.supervisor = Supervisor.objects.create_user(
            username='sup',
            password='root',
            last_login=now(),
            email='sup@gmail.com',
            national_id='43433213',
            supervisor_code='34443835',
            is_accountant=False,
            is_supervisor=True,
            is_people=False,
            user_type=User.Types.supervisor,
            supervisor_license='klenfk/fkvmv/dws',

        )

        self.accountant = Accountant.objects.create_user(
            username='acc',
            password='root',
            email='accountant@gmail.com',
            national_id='43433243',
            accountant_code='34443235',
            accountant_license='klenfk/fkvmv/vlfmvk',
            is_accountant=True,
            is_supervisor=False,
            is_people=False,
            user_type=User.Types.accountant,
            last_login=now()
        )
        self.point = baker.make(PlacePoints, user=self.user)
        self.accept_place = baker.make(AcceptedPlace, supervisor=self.supervisor, mark=self.point)
        self.login = self.client.post('/en/accounts/login/', {'username': 'acc', 'password': 'root'})
        self.token = self.login.data['Token']

        self.login_sup = self.client.post('/en/accounts/login/', {'username': 'sup', 'password': 'root'})
        self.token_sup = self.login_sup.data['Token']
        self.url = reverse('payment')
        self.data = {
            'accountant': self.accountant.id,
            'accept_mark': self.accept_place.id,
            'price': 10000,
        }

    def test_add_payment_url(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')
        response = self.client.post(
            path=self.url,
            data=self.data,
        )
        self.assertEqual(response.status_code, 201)

    def test_add_payment_invalid_accountant(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token_sup}')
        response = self.client.post(
            path=self.url,
            data=self.data,
        )
        self.assertEqual(response.status_code, 403)

    def test_add_payment_auto_save_accountant(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')
        data = {
            'accept_mark': self.accept_place.id,
            'price': 10000,
        }
        response = self.client.post(
            path=self.url,
            data=data,
        )
        self.assertEqual(response.status_code, 201)

    def test_add_payment_is_paid_accepted(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')
        accepted = baker.make(AcceptedPlace, supervisor=self.supervisor, mark=self.point, is_paid=True)
        data = {
            'accept_mark': accepted.id,
            'price': 10000,
        }
        response = self.client.post(
            path=self.url,
            data=data,
        )
        self.assertRaisesRegex(ValueError, 'This mark is paid')
        self.assertEqual(response.status_code, 400)

    def test_return_factor_correctly(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')
        url = reverse('factor')
        response = self.client.get(
            path=url,
        )
        self.assertEqual(response.status_code, 200)

