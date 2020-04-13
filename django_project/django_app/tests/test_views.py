from django.contrib.sessions.middleware import SessionMiddleware
from django.test import RequestFactory, Client

from django.urls import reverse
from rest_framework.test import force_authenticate
from django_app import views
from django_app.models import User
import pytest
import mock


@pytest.mark.django_db
class TestRegistrationView:

    def test_registration_success(self):

        username = 'akshaya'
        email = 'akshayachandorkar29@gmail.com'
        password = 'akshaya29'

        path = reverse('register')
        request = RequestFactory().post(path)
        request.data = {
            'username': username,
            'email': email,
            'password': password,
        }
        response = views.RegistrationView.post(self, request)
        assert response.status_code == 200

    def test_registration_password_not_given(self):

        username = 'akshaya29'
        email = 'akshayachandorkar29@gmail.com'

        path = reverse('register')
        request = RequestFactory().post(path)
        request.data = {
            'username': username,
            'email': email,
            'password': '',
        }
        response = views.RegistrationView.post(self, request)
        assert response.status_code == 200

    def test_registration_username_not_given(self):

        email = 'akshayachandorkar29@gmail.com'
        password = 'akshaya29'

        path = reverse('register')
        request = RequestFactory().post(path)
        request.data = {
            'username': '',
            'email': email,
            'password': password,
        }
        response = views.RegistrationView.post(self, request)
        assert response.status_code == 200


@pytest.mark.django_db
class TestLoginView:

    def test_login_success(self):

        username = 'akshaya'
        password = 'akshaya29'

        user = User.objects.create_user(username=username, email='akshayachandorkar29@gmail.com', password=password,
                                        is_active=True)
        user.save()

        path = reverse('login')
        request = RequestFactory().post(path)
        middleware = SessionMiddleware()
        middleware.process_request(request)
        request.session.save()

        request.data = {
            'username': username,
            'password': password
        }
        # mock.Mock(request)

        response = views.LoginView.post(self, request)
        assert response.status_code == 200

    def test_login_view_invalid_password(self):

        username = 'akshaya'
        password = 'akshaya29'

        user = User.objects.create_user(username=username, email='akshayachandorkar29@gmail.com', password=password,
                                        is_active=True)
        user.save()

        path = reverse('login')
        request = RequestFactory().post(path)
        middleware = SessionMiddleware()
        middleware.process_request(request)
        request.session.save()

        request.data = {
            'username': username,
            'password': '12345'
        }
        # mock.Mock(request)

        response = views.LoginView.post(self, request)
        assert response.status_code == 200

    def test_login_view_invalid_username(self):

        username = 'akshaya'
        password = 'akshaya29'

        user = User.objects.create_user(username=username, email='akshayachandorkar29@gmail.com', password=password,
                                        is_active=True)
        user.save()

        path = reverse('login')
        request = RequestFactory().post(path)
        middleware = SessionMiddleware()
        middleware.process_request(request)
        request.session.save()

        request.data = {
            'username': 'akshaya29',
            'password': password
        }
        # mock.Mock(request)

        response = views.LoginView.post(self, request)
        assert response.status_code == 200


@pytest.mark.django_db
class TestForgotPasswordView:

    def test_forgot_password_success(self):

        username = 'asd'
        email = 'asd@gmail.com'
        password = '123'

        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()

        path = reverse('forgot')
        request = RequestFactory().post(path)
        request.data = {
            'email': email
        }
        response = views.ForgotPassword.post(self, request)
        assert response.status_code == 200

    def test_forgot_password_invalid_email(self):
        username = 'asd'
        email = 'asd@gmail.com'
        password = '123'

        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()

        path = reverse('forgot')
        request = RequestFactory().post(path)
        request.data = {
            'email': None,
        }
        response = views.ForgotPassword.post(self, request)
        assert response.status_code == 200


