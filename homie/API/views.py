import sys
from django.db import models
from django.db.models.fields import EmailField

from django.db.models.query import QuerySet
from django.shortcuts import render, HttpResponse
from .serializer import UserSerializer
from django.http import JsonResponse
from .models import User, Lease, Message
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
from django.core.serializers import serialize

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
def NewLeaseAPI(request):
    if request.method != 'POST':
        return;
    print(request.data)
    return_data = {}

    l_type = request.data['lease_type']
    s_date = request.data['start_date']
    e_date = request.data['end_date']
    rid = getUIDViaEmail(request.data['user_email'])
    try:
        exist_obj = Lease.objects.get(User_id=rid)
    except:
        if (l_type != '' and s_date != '' and e_date != '' and rid != ''):
            lease = Lease.objects.create(User_id_id=rid, lease_type=l_type, start_date=s_date, end_date=e_date)
            lease.save()
            return_data['error_code'] = 0
            response = HttpResponse(json.dumps(return_data), content_type='application/json', status=status.HTTP_201_CREATED)
            return response
        return_data['error_code'] = 2
        response = HttpResponse(json.dumps(return_data), content_type='application/json', status=status.HTTP_400_BAD_REQUEST)
        return response
    return_data['error_code'] = 1
    response = HttpResponse(json.dumps(return_data), content_type='application/json', status=status.HTTP_409_CONFLICT)
    return response

@api_view(http_method_names=['POST'])
@permission_classes((AllowAny,))
@authentication_classes([TokenAuthentication])
@transaction.atomic()
def MessageAPI(request):
    print(request.data)
    return_data = {}

    email_id = getUIDViaEmail(request.data['email'])
    recipient_id = getUIDViaEmail(request.data['recipient'])
    body = request.data['content']

    msg = Message.objects.create(fr_id=email_id, to_id=recipient_id, content=body)
    msg.save()
    return_data['error_code'] = 0
    response = HttpResponse(json.dumps(return_data), content_type='application/json', status=status.HTTP_201_CREATED)
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


def getUIDViaEmail(email):
    return_data = {}

    try:
        exist_obj = User.objects.get(email=email)
    except:
        return
    return exist_obj.uid

def getEmailViaUID(uid):
    try:
        exist_obj = User.objects.get(uid=uid)
    except:
        return
    return exist_obj.email

    
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
def leasing(request):
    template = loader.get_template('Leasing.html')
    return HttpResponse(template.render({}, request))

@api_view(http_method_names=['POST'])
def viewlease(request):
    print(request.data)

    return_data = {}

    try:
        exist_obj = Lease.objects.get(User_id=getUIDViaEmail(request.data['email']));
    except:
        return_data['error_code'] = 1
        response = HttpResponse(json.dumps(return_data, default=str), content_type='application/json',status=status.HTTP_404_NOT_FOUND)
        return response
    return_data['error_code'] = 0
    return_data['unit'] = exist_obj.Unit_id
    return_data['type'] = exist_obj.lease_type
    return_data['start'] = exist_obj.start_date
    return_data['end'] = exist_obj.end_date
    response = HttpResponse(json.dumps(return_data, default=str), content_type='application/json', status=status.HTTP_200_OK)
    return response

@api_view(http_method_names=['POST'])
def viewInbox(request):
    print(request.data)
    return_data = {}

    try:
        inbox = Message.objects.get(to_id=getUIDViaEmail(request.data['email']))
    except:
        return_data['error_code'] = 1
        response = HttpResponse(json.dumps(return_data), content_type='application/json', status=status.HTTP_404_NOT_FOUND)
        return response

    msg_list = []
    for msg in inbox:
        msg_list.append({'from': getEmailViaUID(msg.fr_id), 'body': msg.content})
    
    response = HttpResponse(json.dumps(msg_list), content_type='application/json', status=status.HTTP_200_OK)
    return response

@api_view(http_method_names=['POST'])
def viewOutbox(request):
    print(request.data)
    return_data = {}

    try:
        outbox = Message.objects.filter(fr_id=getUIDViaEmail(request.data['email']))
    except:
        #print("Outbox not found\n")
        return_data['error_code'] = 1
        response = HttpResponse(json.dumps(return_data), content_type='application/json', status=status.HTTP_404_NOT_FOUND)
        return response
    #print("Outbox found successfully\n")
    return_data['error_code'] = 0

    msg_list = []
    for msg in outbox:
        msg_list.append({'to': getEmailViaUID(msg.to_id), 'body': msg.content})
    response = HttpResponse(json.dumps(msg_list), content_type='application/json', status=status.HTTP_200_OK)
    return response

def messages(request):
    template = loader.get_template('messages.html')
    return HttpResponse(template.render({}, request))
