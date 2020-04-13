from django.urls import path
from . import views
# app_name = 'django_app'

urlpatterns = [
    path('register/', views.RegistrationView.as_view(), name="register"),
    path('activate/<token>', views.activate, name='activate'),
    path('login/', views.LoginView.as_view(), name="login"),
    path('logout/', views.LogoutView, name="logout"),
    path('forgot/', views.ForgotPassword.as_view(), name="forgot"),
    path('reset_password/<token>', views.ResetPassword.as_view(), name="reset"),
]