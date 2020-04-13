"""
This is the file containing business logic. All the APIs have been created here
Author: Akshaya Revaskar
Date: 02-04-2020
"""

# importing necessary packages
import os
import jwt
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.http import JsonResponse
from django.shortcuts import render
from django.template.loader import render_to_string
from django_short_url.views import ShortURL
from django_short_url.views import get_surl
from rest_framework import status
from rest_framework.views import APIView
from django.conf import settings
from .validation import Validation
valid = Validation()

from .forms import RegistrationForm, LoginForm, ForgotPasswordForm, ResetForm
from config.redis_service import RedisService

redis = RedisService()  # Object of Redis Class in redis.py file


class RegistrationView(APIView):
    """
    This is the API for registering new user
    """
    # hit will come here on this get method
    def get(self, request, *args, **kwargs):
        form = RegistrationForm()
        # rendering html page to fill the data by user
        return render(request, 'register.html', {'form': form})

    # post method to post data in the form
    def post(self, request, *args, **kwargs):
        # import pdb
        # pdb.set_trace()
        response = {
                        "success": False,
                        "message": "Something Went Wrong!",
                        "data": []
                   }
        try:

            username = request.data['username']
            email = request.data['email']
            password = request.data['password']

            # checking each field is filled
            if username is '' or password is '' or email is '':
                response["message"] = "All fields are mandatory"
                raise Exception

            # validating username
            if not valid.username_validate(username):
                response["message"] = "Length of Username should be greater than 3 and less than 16 and it can not be a number"
                raise ValueError

            # validating email
            if not valid.email_validate(email):
                response["message"] = "Not a valid email id"
                raise ValueError

            # validating password
            if not valid.password_validate(password):
                response["message"] = "Length of password must be 8 or more!!!"
                raise ValueError

            list_of_all_usernames = []
            list_of_all_email = []
            present_users = User.objects.all()
            for i in present_users:
                list_of_all_usernames.append(i.username)
                list_of_all_email.append(i.email)

            # checking if username exists
            for j in list_of_all_usernames:
                if j == username:
                    response["message"] = "User Already Exist..."
                    raise ValueError

            # checking if email exists
            for k in list_of_all_email:
                if k == email:
                    response["message"] = "Email Already Exist..."
                    raise ValueError

            # result = User.objects.get(username=username)
            # if result:
            #     response["message"] = "User Already Exist..."
            #     raise ValueError

            # moving ahead if data is correct
            user = User.objects.create_user(username=username, password=password, email=email)
            if user:
                # setting password in encrypted form
                user.set_password(password)

                user.is_active = False
                user.save()
                response["success"] = True
                response["message"] = "Successfully Registered"

                # generating token with jwt using user id
                token = jwt.encode({'id': user.id}, 'secret', algorithm='HS256').decode('utf-8')

                # converting token in short url to send in the activation email
                surl = get_surl(token)
                surl = surl.split("/")

                # message to send in email
                message = render_to_string('activation.html', {'user': user,
                                           'domain': get_current_site(request).domain,
                                           'token': surl[2]
                                           })

                # subject of the email
                subject = f'Activation Link from {get_current_site(request).domain}'

                # sending mail to the user who got registered to get activated
                send_mail(subject, message, settings.EMAIL_HOST_USER, [user.email], fail_silently=False)

        # catching exceptions
        except ValueError:
            response = response

        except Exception:
            response = response

        # return JsonResponse(data=response, status=status.HTTP_201_CREATED)
        # return render(request, 'register.html', {'form': form})
        return render(request, 'response.html', {'response': response["message"]})


# function to activate user
def activate(request, token):

    # import pdb
    # pdb.set_trace()
    response = {"success": False, "message": "Something Went Wrong", "data": []}
    try:
        # getting short token from database
        token1 = ShortURL.objects.get(surl=token)
        # converting short url into long url
        token = token1.lurl
        # decoding token into payload
        payload = jwt.decode(token, 'secret', algorithm=['HS256'])
        # getting id from payload
        uid = payload['id']
        # getting user data of the same user
        user = User.objects.get(pk=uid)

        if user:
            # activating user
            user.is_active = True
            user.save()
            response = {"success": True, "message": "Your account is activated Successfully!"}

    except Exception:
        response = response

    # return JsonResponse(data=response, status=status.HTTP_200_OK)
    return render(request, 'response.html', {'response': response["message"]})


class LoginView(APIView):
    """
    This is the API for Login User who is already registered
    """

    def get(self, request, *args, **kwargs):
        form = LoginForm()
        return render(request, 'login.html', {'form': form})

    def post(self, request):
        response = {
            "success": False,
            "message": 'Unable to Login',
            "data": []
        }
        try:
            # import pdb
            # pdb.set_trace()

            # getting data from request object
            username = request.data.get('username')
            password = request.data.get('password')

            # checking user of the same username and password present in the database by django's default authentication system
            user = authenticate(username=username, password=password)

            # user = User.objects.get(username=username)

            # moving if user found
            if user and user.is_active:
                # if user is not None:
                # generating token with user id
                token = jwt.encode({'id': user.id}, 'secret', algorithm='HS256').decode('utf-8')

                response["success"] = True
                response["message"] = 'Login Successful!!!'
                response["data"] = [token]

                # setting token and user id in the redis to access frequently
                redis.set(user.id, token)
            else:
                response["message"] = "Incorrect Username/Password OR user is not activated"
                raise Exception

        except Exception:
            response = response

        # return JsonResponse(data=response, status=status.HTTP_200_OK)
        return render(request, 'response.html', {'response': response["message"]})


class LogoutView(APIView):
    """
    API for logout the user who is logged in
    """

    def post(self, request):
        response = {
            "success": False,
            "message": "Something went wrong",
            "data": []
        }
        # import pdb
        # pdb.set_trace()
        # getting token from the headers
        token = request.META['HTTP_TOKEN']

        # decoding token to generate payload
        payload = jwt.decode(token, 'secret', algorithm='HS256')

        # getting id of the user who is logged in from payload
        user_id = payload.get('id')

        # deleting the user from redis cache
        redis.delete(user_id)

        response["success"] = True
        response["message"] = "User Logged Out"
        response["data"] = []

        # return JsonResponse(data=response, status=status.HTTP_200_OK)
        return render(request, 'response.html', {'response': response["message"]})


class ForgotPassword(APIView):

    def get(self, request, *args, **kwargs):
        form = ForgotPasswordForm()
        return render(request, 'forgot.html', {'form': form})

    def post(self, request):
        form = ForgotPasswordForm(data=request.data)

        # import pdb
        # pdb.set_trace()

        response = {
                      "success": False,
                      "message": "User not Found",
                      "data": []
                   }
        try:
            email = request.data['email']
            username = request.data['username']
            user = User.objects.get(username=username, email=email)

            token = jwt.encode({'id': user.id}, 'secret', algorithm='HS256').decode('utf-8')
            surl = get_surl(token)
            surl = surl.split('/')

            message = render_to_string('forgot_mail.html', {
                'user': user,
                'domain': get_current_site(request).domain,
                'token': surl[2]
            })
            subject = f'Reset Password Link from {get_current_site(request).domain}'
            send_mail(subject, message, settings.EMAIL_HOST_USER, [user.email], fail_silently=False)

            response["success"] = True
            response["message"] = "We have sent you a TOKEN,Please check your registered E-Mail ID"
            response["data"] = token
        except Exception:
            response = response

        # return JsonResponse(data=response, status=status.HTTP_200_OK)
        return render(request, 'response.html', {'response': response["message"]})


class ResetPassword(APIView):

    def get(self, request, *args, **kwargs):
        form = ResetForm()
        return render(request, 'reset.html', {'form': form})

    def post(self, request, token):
        response = {
            "success": False,
            "message": "User not Found",
            "data": []
        }
        try:
            # import pdb
            # pdb.set_trace()
            old_password = request.data['old_password']
            new_password = request.data['new_password']
            conform_password = request.data['conform_password']

            token = ShortURL.objects.get(surl=token).lurl

            payload = jwt.decode(token, 'secret', algorithm='HS256')
            id = payload['id']
            user = User.objects.get(pk=id)

            if new_password == conform_password:
                user.set_password(new_password)
                user.save()

                response["success"] = True
                response["message"] = "Your password is reset Successfully"
                response["data"] = [token]
            else:
                response["message"] = "new password and conform password should match"

        except Exception:
            response = response

        # return JsonResponse(data=response, status=status.HTTP_200_OK)
        return render(request, 'response.html', {'response': response["message"]})
