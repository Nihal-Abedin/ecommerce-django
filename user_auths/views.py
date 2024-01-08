from django.shortcuts import render
from user_auths.models import User, Profile
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from user_auths.serializer import MyTokenObtainPairSerializer, RegisterSerializer, UserSerializer
import shortuuid


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer
    # serializer_class.get_token()


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer


def generate_otp():
    uuid_key = shortuuid.uuid()
    unique_key = uuid_key[:7]

    return unique_key


class ResetUserPasswordEmail(generics.RetrieveAPIView):
    permission_classes = (AllowAny,)
    serializer_class = UserSerializer

    def get_object(self):
        email = self.kwargs['email']
        user = User.objects.get(email=email)

        print(user)

        if user:
            user.otp = generate_otp()
            user.save()

            user_otp = user.otp
            user_id = user.pk
            link = f'http://127.0.0.1:30001/create-password?otp={user_otp}&id={user_id}'
            print(link)
            # SEND EMAIL
        return user


class PasswordChangeView(generics.CreateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        payload = request.data

        otp = payload['otp']
        password = payload['password']
        uid = payload['uuid']

        user = User.objects.get(otp=otp, id=uid)

        if user:
            user.set_password(password)
            user.otp = ''
            user.save()

            return Response({"message": "Password changed successfully!"}, status=status.HTTP_201_CREATED)
        else:
            return Response({"message": "User doesn't exists"}, status=status.HTTP_404_NOT_FOUND)
