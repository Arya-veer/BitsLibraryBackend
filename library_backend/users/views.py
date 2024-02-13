from django.contrib.auth.models import User 
from django.contrib.auth import login,logout

from rest_framework.views import APIView
from rest_framework.permissions import AllowAny,IsAuthenticated
from rest_framework.response import Response
from rest_framework import status,generics

from rest_framework_simplejwt.tokens import RefreshToken

from users.permissions import StaffPermission

import firebase_admin
from firebase_admin import auth

from .models import *
from .serializers import *

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
        profile = UserProfile.objects.filter(auth_user=user).first()
        if not user or not profile:
            return Response({"message": "Email not registered, Please contact Librarian for support"},status=status.HTTP_400_BAD_REQUEST)
        login(request,user)
        return Response({"message": "Login Successful","data":UserProfileSerializer(profile).data},status=status.HTTP_200_OK)
        # except Exception as e:
        #     return Response({"message": str(e)},status=status.HTTP_400_BAD_REQUEST

class UserLogoutAPI(APIView):  
    
        permission_classes = (IsAuthenticated,)
    
        def post(self, request):
            logout(request)
            return Response({"message": "Logout Successful"},status=status.HTTP_200_OK)


class UserProfileAPI(APIView):
    
        permission_classes = (IsAuthenticated,)
    
        def get(self, request):
            user = request.user
            # print(request.COOKIES)
            profile = UserProfile.objects.filter(auth_user=user).first()
            if not profile:
                return Response({"message": "User Not Found"},status=status.HTTP_400_BAD_REQUEST)
            serializer = UserProfileSerializer(profile)
            return Response(serializer.data,status=status.HTTP_200_OK)

class PhoneNumberUpdateAPI(APIView):

    permission_classes = (IsAuthenticated,)

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

class AddItemAPI(generics.CreateAPIView):
    permission_classes = (StaffPermission,)
    serializer_class = ItemSerializer

class ItemListAPI(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = ItemSerializer
    
    def get_queryset(self):
        items = Item.objects.all()#.exclude(id__in = Claim.objects.filter(is_approved = True).exclude(user = self.request.user.profile).values_list('item__id',flat=True))
        return items.order_by('-dt')
    
class StaffItemListAPI(generics.ListAPIView):
    permission_classes = (StaffPermission,)
    serializer_class = StaffItemSerializer

    def get_queryset(self):
        type = self.request.query_params.get("type", "Pending")
        claimed_items = Claim.objects.filter(is_approved = True).values_list('item__id',flat=True).distinct()
        if type == "Pending":
            return Item.objects.exclude(id__in = claimed_items).order_by('-dt')
        return Item.objects.filter(id__in = claimed_items).order_by('-dt')

class ClaimedItemsAPI(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = ClaimSerializer
    
    def get_queryset(self):
        user = self.request.user
        items = Claim.objects.filter(user=user)
        return items

class StaffClaimedItemsAPI(generics.ListAPIView):
    permission_classes = (StaffPermission,)
    serializer_class = StaffClaimSerializer

    def get_queryset(self):
        item = Item.objects.get(id=self.request.query_params.get('item_id',-1))
        return Claim.objects.filter(item=item).order_by('-date')
    
    def list(self, request, *args, **kwargs):
        try:
            return super().list(request, *args, **kwargs)
        except Exception as e:
            return Response({"message": str(e)},status=status.HTTP_400_BAD_REQUEST)
    
class ApproveClaimAPI(APIView):
    permission_classes = (StaffPermission,)
    
    def post(self,request):
        if "claim_id" not in request.data:
            return Response({'message': 'Insufficient Request Parameters.'},status=status.HTTP_400_BAD_REQUEST)
        claim_id = request.data['claim_id']
        claims = Claim.objects.filter(id=claim_id,is_approved=False)
        if not claims.exists():
            return Response({"message": "Claim Not Found"},status=status.HTTP_400_BAD_REQUEST)
        claim = claims.first()
        if claim.item.claims.filter(is_approved=True).exists():
            return Response({"message": "Item already claimed"},status=status.HTTP_400_BAD_REQUEST)
        claim.is_approved = True
        claim.save()
        return Response({"message": "Claim Approved"},status=status.HTTP_200_OK)

class ClaimItemAPI(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self,request):
        if "item_id" not in request.data:
            return Response({'message': 'Insufficient Request Parameters.'},status=status.HTTP_400_BAD_REQUEST)
        item_id = request.data['item_id']
        user = request.user.profile
        items = Item.objects.filter(id=item_id)
        if not items.exists():
            return Response({"message": "Item Not Found"},status=status.HTTP_400_BAD_REQUEST)
        item = items.first()
        if Claim.objects.filter(user=user,item=item).exists():
            return Response({"message": "You have already claimed this item"},status=status.HTTP_400_BAD_REQUEST)
        if Claim.objects.filter(item=item,is_approved=True).exists():
            return Response({"message": "Item already claimed"},status=status.HTTP_400_BAD_REQUEST)
        try:
            claim = Claim.objects.create(user=user,item=item)
            return Response({"message": "Item Claimed! You can check the status later"},status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"message": str(e)},status=status.HTTP_400_BAD_REQUEST)


class ArticleBookRequestListCreateAPI(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = ArticleBookRequestSerializer

    def get_queryset(self):
        user = self.request.user
        type_doc = self.request.query_params.get('type_doc', 'Article')
        requests = ArticleBookRequest.objects.filter(user=user.profile,type_doc=type_doc)
        return requests


class FreeBookListAPI(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = FreeBookSerialzer

    def get_queryset(self):
        books = FreeBook.objects.all()
        return books
    
class FreeBookPickAPI(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = FreeBookPickSerializer
    
    def get_queryset(self):
        return FreeBookPick.objects.filter(user=self.request.user.profile)

    def post(self,request):
        if "book_id" not in request.data:
            return Response({'message': 'Insufficient Request Parameters.'},status=status.HTTP_400_BAD_REQUEST)
        book_id = request.data['book_id']
        user = request.user
        books = FreeBook.objects.filter(id=book_id)
        if not books.exists():
            return Response({"message": "Book Not Found"},status=status.HTTP_400_BAD_REQUEST)
        book = books.first()
        if FreeBookPick.objects.filter(user=user.profile,book=book,status = "Pending").exists():
            return Response({"message": "You have already claimed this book"},status=status.HTTP_400_BAD_REQUEST)
        if FreeBookPick.objects.filter(user=user.profile,book=book,status = "Rejected").exists():
            return Response({"message": "You have already claimed this book and it was rejected"},status=status.HTTP_400_BAD_REQUEST)
        if FreeBookPick.objects.filter(book=book,status="Approved",user=user.profile).exists():
            return Response({"message": "Book already claimed by you"},status=status.HTTP_400_BAD_REQUEST)
        if FreeBookPick.objects.filter(book=book,status="Approved").exists():
            return Response({"message": "Book already claimed"},status=status.HTTP_400_BAD_REQUEST)
        try:
            claim = FreeBookPick.objects.create(user=user.profile,book=book)
            return Response({"message": "Book Claimed! You can check the status later"},status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"message": str(e)},status=status.HTTP_400_BAD_REQUEST)

class CheckProfileExists(APIView):
    permission_classes = (AllowAny,)

    def post(self,request):
        if "email" not in request.data:
            return Response({'message': 'Insufficient Request Parameters.'},status=status.HTTP_400_BAD_REQUEST)
        email = request.data['email']
        users = User.objects.filter(email=email)
        if not users.exists():
            return Response({"message": "User does not exist"},status=status.HTTP_400_BAD_REQUEST)
        user = users.first()
        up = UserProfile.objects.filter(auth_user=user)
        if not up.exists():
            return Response({"message": "User does not exist"},status=status.HTTP_400_BAD_REQUEST)
        return Response({"message": "User exists","data":UserProfileSerializer(up.first()).data},status=status.HTTP_200_OK)