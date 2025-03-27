from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from rest_framework_simplejwt.tokens import RefreshToken
from django.middleware.csrf import get_token
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample
from django.views.decorators.csrf import csrf_exempt
from .serializers import (
    SignUpSerializer,
    LoginSerializer,
    PasswordSerializer
)

@csrf_exempt
class Login(APIView):

    @extend_schema(
        request=LoginSerializer
    )
    def post(self, request):
        try:
            user = authenticate(username=request.data.get('username'), password=request.data.get('password'))
            if user is not None:
                refresh = RefreshToken.for_user(user)
                csrfToken = get_token(request)
                login(request, user)
                return Response(
                    {
                        'id': user.pk,
                        'username': user.username,
                        'email': user.email,
                        'refresh': str(refresh),
                        'access': str(refresh.access_token),
                        'csrfToken': csrfToken
                    },
                    status=status.HTTP_200_OK
                )
            else:
                return Response('Failed to login, check your credentials', status=status.HTTP_401_UNAUTHORIZED)
        except:
            return Response('There was an unexpected error, try again', status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class SignUp(APIView):
    @extend_schema(
        request=SignUpSerializer
    )
    def post(self, request):
        try:
            user = User.objects.create_user(request.data.get('username'), 
                                        request.data.get('email'), 
                                        request.data.get('password')
                                        )
            user.save()
            return Response('User creatred succesfully', status=status.HTTP_201_CREATED)
        except:
            return Response('Failed to create user', status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@extend_schema(
    request=PasswordSerializer
)
class ChangePassword(APIView):
    def put(self, request, email):
        try:
            user = User.objects.get(email=email)
            user.set_password(request.data.get('password'))
            user.save()
            return Response('Your password has been changed succesfully', status=status.HTTP_200_OK)
        except:
            return Response('There was an unexpected error, try again', status=status.HTTP_505_HTTP_VERSION_NOT_SUPPORTED)