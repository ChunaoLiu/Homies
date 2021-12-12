import sys
from django.db import models
from django.db.models.fields import EmailField

from django.db.models.query import QuerySet
from django.shortcuts import render, HttpResponse
from .serializer import UserSerializer
from django.http import JsonResponse
from .models import User
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import APIView
from django.template import loader
from django.shortcuts import render
import json
from django.http import JsonResponse
from django.db import transaction

from django.contrib.auth import authenticate, login, logout, get_user_model
from rest_framework.authentication import TokenAuthentication, BasicAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.decorators import APIView, permission_classes, authentication_classes, api_view
from rest_framework.permissions import IsAuthenticated, AllowAny

from django.db import transaction

# Create your views here.
class AllUserList(APIView):
    def get(self, request):
        users = User.objects.all()
        Serializer = UserSerializer(users, many=True)
        return Response(Serializer.data)
    

class SignupAPI(APIView):
    def post(self, request):
        print(request.data)

        return_data = {}
        
        New_name = request.data['username']
        New_password = request.data['password']
        New_email = request.data['email']
        New_age = request.data['age']
        New_gender = request.data['gender']
        try:
            exist_obj = User.objects.get(email=New_email)
        except:
            if (New_email != '' and New_password != '' and New_name != '' and New_gender != '' and New_age != ''):
                userModel = get_user_model()
                user_auth = userModel.objects.create_user(username=New_email, password=New_password)
                user_auth.save()
                new_User = User.objects.create(name=New_name, password=New_password, email=New_email, age=New_age, gender=New_gender, pk=user_auth.pk)
                new_User.save()
                return_data['error_code'] = 0
                response = HttpResponse(json.dumps(return_data),
                                        content_type='application/json', status=status.HTTP_201_CREATED)
                return response
            return_data['error_code'] = 2
            response = HttpResponse(json.dumps(return_data),
                                        content_type='application/json', status=status.HTTP_400_BAD_REQUEST)
            return response
        
        return_data['error_code'] = 1
        response = HttpResponse(json.dumps(return_data),
                                content_type='application/json', status=status.HTTP_409_CONFLICT)
        return response

@api_view(http_method_names=['POST'])
@permission_classes((AllowAny,))
@authentication_classes([TokenAuthentication])
@transaction.atomic()
def UserLogIn(request):
    print(request.data)

    return_data = {}

    Login_email = request.data['email']
    Login_password = request.data['password']

    try:
        exist_obj = User.objects.get(email=Login_email, password=Login_password)
    except:
        return_data['error_code'] = 1
        response = HttpResponse(json.dumps(return_data),
                            content_type='application/json', status=status.HTTP_401_UNAUTHORIZED)
        return response
    
    return_data['error_code'] = 0
    response = HttpResponse(json.dumps(return_data),
                        content_type='application/json', status=status.HTTP_200_OK)
    return response
        

class DeleteUserByID(APIView):
    def delete(self, request, uid):
        target = User.objects.get(pk=uid)
        if (target == None):
            return Response(status=status.HTTP_404_NOT_FOUND)
        target.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(http_method_names=['POST'])
@permission_classes((AllowAny,))
@authentication_classes([TokenAuthentication])
@transaction.atomic()
def getNameViaEmail(request):
    print(request.data)

    return_data = {}

    email = request.data['email']

    try:
        exist_obj = User.objects.get(email=email)
    except:
        return_data['error_code'] = 1
        response = HttpResponse(json.dumps(return_data),
                            content_type='application/json', status=status.HTTP_404_NOT_FOUND)
        return response
    
    return_data['error_code'] = 0
    return_data['name'] = exist_obj.name
    response = HttpResponse(json.dumps(return_data),
                            content_type='application/json', status=status.HTTP_200_OK)
    return response

    
def index(request):
    template = loader.get_template('index.html')
    return HttpResponse(template.render({}, request))

def signup(request):
    template = loader.get_template('addUserCol.html')
    return HttpResponse(template.render({}, request))

def test(request):
    template = loader.get_template('testing.html')
    return HttpResponse(template.render({}, request))

def homePage(request):
    template = loader.get_template('homePage.html')
    return HttpResponse(template.render({}, request))