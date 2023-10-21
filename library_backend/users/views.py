from django.contrib.auth.models import User 

from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status

from rest_framework_simplejwt.tokens import RefreshToken

import firebase_admin
from firebase_admin import auth

from .models import *

import library_backend.keyconfig as senv

import json

# Create your views here.

class UserLoginAPI(APIView):


    def post(self, request):
        if not firebase_admin._apps:
            cred = firebase_admin.credentials.Certificate(senv.CREDENTIALS_JSON)
            default_app = firebase_admin.initialize_app(cred)
        if "firebase_id" in request.data:
            firebase_id = request.data['firebase_id']
        else:
            return Response({'message': 'Insufficient Request Parameters.'},status=status.HTTP_400_BAD_REQUEST)
        # try:
        firebase_user = auth.get_user(firebase_id)
        user = User.objects.filter(email=firebase_user.email)
        user = user.first()

        if not user or not UserProfile.objects.filter(auth_user=user).exists():
            return Response({"message": "Email not registered, Please contact Librarian for support"},status=status.HTTP_400_BAD_REQUEST)
        refresh = RefreshToken.for_user(user)
        response = Response({"access":str(refresh.access_token),'phone_number':user.profile.phone_number},status.HTTP_200_OK)
        response.set_cookie('jwt', str(refresh.access_token), httponly=False, secure=True, samesite='None')
        return response
        # except Exception as e:
        #     return Response({"message": str(e)},status=status.HTTP_400_BAD_REQUEST)

class PhoneNumberUpdateAPI(APIView):

    def post(self, request):
        if "phone_number" not in request.data:
            return Response({'message': 'Insufficient Request Parameters.'},status=status.HTTP_400_BAD_REQUEST)
        phone_number = request.data['phone_number']
        user = request.user
        try:
            user.profile.phone_number = phone_number
            user.profile.save()
            return Response({"message": "Phone Number Updated Successfully"},status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"message": str(e)},status=status.HTTP_400_BAD_REQUEST)