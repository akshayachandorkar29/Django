from django.urls import reverse, resolve


class TestUrls:

    """
    Testing For Urls match.
    Reverse() is being used to generate the Url from the view name
    Resolve() is being used to match the view_name to the Url path given by Reverse()
    """

    def test_register_url(self):

        path = reverse('register')
        assert resolve(path).view_name == 'register'

    def test_activate_url(self):
        path = reverse('activate', kwargs={'token': '3zV34sAvfCaCY8yqwz8RHt'})
        assert resolve(path).view_name == 'activate'

    def test_login_url(self):
        path = reverse('login')
        assert resolve(path).view_name == 'login'

    def test_logout_url(self):
        path = reverse('logout')
        assert resolve(path).view_name == 'logout'

    def test_forgot_password_url(self):
        path = reverse('forgot')
        assert resolve(path).view_name == 'forgot'

    def test_rest_url(self):
        path = reverse('reset', kwargs={'token': '3zV34sAvfCaCY8yqwz8RHt'})
        assert resolve(path).view_name == 'reset'
