from unittest import mock
from datetime import datetime, timedelta
from django.urls import reverse
from django.utils.timezone import now
from rest_framework.test import APITestCase, APIClient, APIRequestFactory
import json

from accountants.models import Accountant
from accounts.models import User, OtpCode
from accounts.views import EmployeeUpdate
from supervisors.models import Supervisor
from django.core import mail
from django_rest_passwordreset.models import ResetPasswordToken


class AccountRegisterTest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.reg_url = '/en/accounts/register/'

    def test_register_url(self):
        user = {
            'username': 'root',
            'password': 'root',
            'password2': 'root',
            'email': 'root@gmail.com'
        }

        response = self.client.post(
            self.reg_url,
            data=user,
        )

        self.assertEqual(response.status_code, 201)

    def test_register_invalid_email(self):
        user = {
            'username': 'root',
            'password': 'root',
            'password2': 'root',
            'email': 'root'
        }
        response = self.client.post(
            self.reg_url,
            data=user,
        )
        self.assertEqual(response.status_code, 400)

    def test_not_match_password(self):
        user = {
            'username': 'root',
            'password': 'root2',
            'password2': 'root',
            'email': 'root@gmail.com'
        }

        response = self.client.post(
            self.reg_url,
            data=user,
        )
        self.assertRaisesRegex(ValueError, 'Password must be match')

    def test_duplicate_username(self):
        User.objects.create_user(
            username='root',
            password='root',
            email='root@gmail.com'
        )

        user = {
            'username': 'root',
            'password': 'root',
            'password2': 'root',
            'email': 'root4@gmail.com'
        }
        response = self.client.post(
            self.reg_url,
            data=user,
        )
        self.assertEqual(User.objects.filter(username='root').count(), 1)

    def test_duplicate_email(self):
        User.objects.create_user(
            username='root',
            password='root',
            email='root@gmail.com'
        )

        user = {
            'username': 'root5',
            'password': 'root',
            'password2': 'root',
            'email': 'root@gmail.com'
        }
        response = self.client.post(
            self.reg_url,
            data=user,
        )
        self.assertRaisesRegex(ValueError, 'This Email already exists')


class AccountsLoginTest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = '/en/accounts/login/'
        self.user = User.objects.create_user(
            username='root',
            password='root',
            email='root@gmail.com'
        )

        self.supervisor = Supervisor.objects.create_user(
            username='sup',
            password='root',
            email='supervisor@gmail.com',
            national_id='434343',
            supervisor_code='34435',
            supervisor_license='klenfk/fkvmv/vklfmvk'
        )
        self.supervisor2 = Supervisor.objects.create_user(
            username='sup2',
            password='root',
            email='supervisor2@gmail.com',
            national_id='43443',
            supervisor_code='3443',
            supervisor_license='klenfk/fkvmv/flkf',
            last_login=now(),
        )

        self.accountant = Accountant.objects.create_user(
            username='acc',
            password='root',
            email='accountant@gmail.com',
            national_id='43433243',
            accountant_code='34443235',
            accountant_license='klenfk/fkvmv/vlfmvk'
        )
        self.accountant2 = Accountant.objects.create_user(
            username='acc2',
            password='root',
            email='accountant2@gmail.com',
            national_id='4345343',
            accountant_code='3443443',
            accountant_license='klenfk/fkvmv/flf',
            last_login=now(),
        )

        self.data = {
            'username': 'root',
            'password': 'root',
        }

    def test_login_url(self):
        response = self.client.post(
            self.url,
            data=self.data,
        )
        self.assertEqual(response.status_code, 200)

    def test_valid_username(self):
        response = self.client.post(
            self.url,
            data={
                'username': 'root2',
                'password': 'root',
            }
        )
        self.assertRaisesRegex(ValueError, 'dos not exist')

    def test_valid_password(self):
        response = self.client.post(
            self.url,
            data={
                'username': 'root',
                'password': 'root2',
            }
        )
        self.assertRaisesRegex(ValueError, 'dos not exist')

    def test_login_supervisor(self):
        response = self.client.post(
            self.url,
            data={
                'username': 'sup',
                'password': 'root',
            }
        )
        sup: Supervisor = Supervisor.objects.filter(username='sup').first()
        self.assertContains(response, 'set a new password')

    def test_login_supervisor_with_las_login(self):
        response = self.client.post(
            self.url,
            data={
                'username': 'sup2',
                'password': 'root',
            }
        )

        self.assertEqual(
            response.status_code, 200
        )

    def test_login_accountant(self):
        response = self.client.post(
            self.url,
            data={
                'username': 'acc',
                'password': 'root',
            }
        )
        sup: Accountant = Accountant.objects.filter(username='acc').first()
        self.assertContains(response, 'set a new password')

    def test_login_accountant_with_las_login(self):
        response = self.client.post(
            self.url,
            data={
                'username': 'acc2',
                'password': 'root',
            }
        )

        self.assertEqual(
            response.status_code, 200
        )


# datetime = mock.Mock()
# datetime.datetime.now().minute.return_value = 0


class AccountsLoginVerifyTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='root',
            password='root',
            email='root@gmai.com',
        )
        self.client = APIClient()
        self.url = '/en/accounts/login/verify/'

        # self.login = self.client.post('/en/accounts/login/', data={'username': 'root', 'password': 'root'})

    def test_login_verify_wrong_opt_code(self):
        response = self.client.post(
            path=self.url,
            data={'code': 3423}
        )
        self.assertEqual(response.status_code, 400)

    def test_login_verify_correct_otp_code(self):
        self.login = self.client.post('/en/accounts/login/', data={'username': 'root', 'password': 'root'})
        code: OtpCode = OtpCode.objects.first()
        response = self.client.post(
            path=self.url,
            data={'code': code.code}
        )
        self.assertEqual(response.status_code, 200)

    @mock.patch('accounts.views.datetime')
    def test_expired_code(self, mock_date):
        self.login = self.client.post('/en/accounts/login/', data={'username': 'root', 'password': 'root'})
        current_time = datetime.now()
        future_time = current_time + timedelta(minutes=2)
        mock_date.datetime.now.return_value = future_time
        code: OtpCode = OtpCode.objects.all()

        response = self.client.post(
            path=self.url,
            data={'code': code.first().code}
        )
        self.assertEqual(code.count(), 0)


class AccountsUpdateEmployeeTest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        # self.user = User.objects.create_user(
        #     username='root',
        #     password='root',
        #     email='root@gmail.com'
        # )

        self.supervisor = Supervisor.objects.create(
            username='sup',
            email='supervisor@gmail.com',
            national_id='434343',
            supervisor_code='34435',
            supervisor_license='klenfk/fkvmv/vklfmvk',
            is_supervisor=True,
            is_accountant=False,
            is_people=False,
            user_type=User.Types.supervisor,
        )
        self.supervisor.set_password('root')
        self.supervisor.save()

        self.accountant = Accountant.objects.create(
            username='acc',
            email='accountant@gmail.com',
            national_id='43433243',
            accountant_code='34443235',
            accountant_license='klenfk/fkvmv/vlfmvk',
            is_accountant=True,
            is_supervisor=False,
            is_people=False,
            user_type=User.Types.accountant,
        )
        self.accountant.set_password('root')
        self.accountant.save()

    def test_update_correctly(self):
        pk = self.supervisor.id
        self.url = reverse('update_employee', args=[pk])
        data = {
            'password': 'root',
            'new_password': 'rootii',
            'confirm_new': 'rootii',
        }
        response = self.client.put(
            self.url,
            data=data,
        )
        self.assertEqual(response.status_code, 200)


class AccountsUpdateTest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='root',
            password='root',
            email='root@gmail.com'
        )
        pk = self.user.id
        self.url = reverse('update_user', args=[pk])

        self.login = self.client.post('/en/accounts/login/', {'username': 'root', 'password': 'root'})
        code = OtpCode.objects.first()
        self.ver = self.client.post('/en/accounts/login/verify/', {'code': code.code})
        self.token = self.ver.data['token']

    def test_update_user_url(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 405)

    def test_update_user_valid_data(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')

        data = {
            'username': 'root',
            'password': 'root',
            'first_name': 'ali',
            'last_name': 'sol',
            'email': 'rootali@gmail.com',
        }

        response = self.client.put(self.url, data=data)
        self.assertEqual(response.status_code, 200)

    def test_update_user_with_out_authorization(self):
        # self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}nn')
        data = {
            'username': 'root',
            'password': 'root',
            'first_name': 'ali',
            'last_name': 'sol',
            'email': 'rootali@gmail.com',
        }
        response = self.client.put(self.url, data=data)
        self.assertEqual(response.status_code, 401)

    def test_update_user_invalid_data(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')
        data = {
            'username': 'root',
            'password': 'root',
            'first_name': 'ali',
            'last_name': 'sol',
            'email': 'rootaligmailcom',
            'middle_name': 'reza',
        }

        response = self.client.put(self.url, data=data)
        self.assertFalse('middle_name' in response.data)


class AccountsLogoutTest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='root',
            password='root',
            email='root@gmail.com'
        )
        pk = self.user.id
        self.url = reverse('logout')

        self.login = self.client.post('/en/accounts/login/', {'username': 'root', 'password': 'root'})
        code = OtpCode.objects.first()
        self.ver = self.client.post('/en/accounts/login/verify/', {'code': code.code})
        self.token = self.ver.data['token']

    def test_logout_url(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')
        response = self.client.post(
            self.url,
        )
        self.assertEqual(response.status_code, 200)

    def test_user_login_before_logout(self):
        response = self.client.post(
            self.url,
        )
        self.assertEqual(response.status_code, 401)


class AccountsResetPasswordTest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='root',
            password='root',
            email='root@gmail.com'
        )
        self.url = '/en/accounts/pass-reset/'

    def test_reset_password_url(self):
        response = self.client.post(
            self.url,
            data={
                'email': 'root@gmail.com'
            }
        )
        self.assertEqual(response.status_code, 200)

    def test_reset_password_invalid_email(self):
        response = self.client.post(
            self.url,
            data={
                'email': 'rootgmailcom'
            }
        )
        self.assertEqual(response.status_code, 400)

    def test_reset_password_email_does_not_exists(self):
        response = self.client.post(
            self.url,
            data={
                'email': 'root3@gmail.com'
            }
        )
        self.assertEqual(response.status_code, 400)

    def test_reset_password_check_sen_mail(self):
        response = self.client.post(
            self.url,
            data={
                'email': 'root@gmail.com'
            }
        )
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, 'Reset')


class AccountsResetPasswordConfirmToken(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='root',
            password='root',
            email='root@gmail.com'
        )
        self.url = '/en/accounts/pass-reset/'
        self.reset_pass = self.client.post(
            self.url,
            data={
                'email': 'root@gmail.com'
            }
        )

    def test_confirm_reset_password(self):
        token: ResetPasswordToken = ResetPasswordToken.objects.first()
        arg = token.key
        url = reverse('password_reset_confirm', args=[arg])
        response = self.client.post(
            path=url,
            data={
                'password': 'rootroot',
                'token': arg
            }
        )
        self.assertEqual(response.status_code, 200)
