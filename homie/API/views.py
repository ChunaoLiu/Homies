import sys
from django.db import models
from django.db.models.fields import EmailField

from django.db.models.query import QuerySet
from django.shortcuts import render, HttpResponse
from .serializer import UserSerializer
from django.http import JsonResponse
from .models import User, Lease, Message, Dorm, Unit, WorkOrder
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
from django.db import connection

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


@api_view(http_method_names=['GET'])
@permission_classes((AllowAny,))
def getTotalNumPeople(request):
    return_data = {}

    num_ppl = User.objects.raw('SELECT uid, COUNT(*) FROM API_user GROUP BY uid;')
    print(num_ppl)
    print(len(list(num_ppl)))
    return_data['output'] = len(list(num_ppl))
    return HttpResponse(json.dumps(return_data),
                            content_type='application/json', status=status.HTTP_200_OK)

@api_view(http_method_names=['POST'])
@permission_classes((AllowAny,))
def getRA_API(request):
    return_data = {}
    senderEmail = request.data['senderEmail']
    
    user = User.objects.raw('SELECT uid from API_user WHERE email=\'' + senderEmail + '\';')
    for p in user:
        if p.uid == None:
            return_data['error_code'] = 1
            return HttpResponse(json.dumps(return_data),
                            content_type='application/json', status=status.HTTP_404_NOT_FOUND)

    RA = User.objects.raw('SELECT uid, RA_id as RA from API_user WHERE email=\'' + senderEmail + '\';')
    for p in RA:
        if (p.RA is None):
            return_data['is_RA'] = False
        else:
            return_data['is_RA'] = True
    
    Res = User.objects.raw('SELECT uid, Unit_id_id as unit FROM API_user WHERE email=\'' + senderEmail + '\';')
    for p in Res:
        if (p.unit is None):
            return_data['unit'] = False
        else:
            unit = Unit.objects.raw('SELECT Unit_id, unit_name FROM API_unit WHERE Unit_id=\'' + p.unit + '\';')
            for s in unit:
                return_data['unit'] = s.unit_name
                
    return_data['error_code'] = 0        
    return HttpResponse(json.dumps(return_data),
                            content_type='application/json', status=status.HTTP_200_OK)


@api_view(http_method_names=['POST'])
@transaction.atomic()
def set_Unit(request):
    print (request.data)

    return_data = {}

    try:
        dorm = Dorm.objects.get(Dorm_id=1)
    except:
        return_data['error_code'] = 1
        return HttpResponse(json.dumps(return_data),
                            content_type='application/json', status=status.HTTP_404_NOT_FOUND)
    
    new_unit = Unit.objects.create(unit_name='A-123', num_ppl=0, max_ppl=4, has_kitchen=True, has_laundry=True, Dorm_id=dorm)
    return_data['error_code'] = 0
    return HttpResponse(json.dumps(return_data),
                            content_type='application/json', status=status.HTTP_200_OK)

@api_view(http_method_names=['POST'])
@transaction.atomic()
def order_add(request):
    print (request.data)

    return_data = {}

    user_Email = request.data['email']
    unit_id = request.data['unit_id']
    description = request.data['description']

    try:
        unit = Unit.objects.get(Unit_id=unit_id)
    except:
        return_data['error_code'] = 1
        return HttpResponse(json.dumps(return_data),
                            content_type='application/json', status=status.HTTP_404_NOT_FOUND)

    try:
        user = User.objects.get(email=user_Email)
    except:
        return_data['error_code'] = 2
        return HttpResponse(json.dumps(return_data),
                            content_type='application/json', status=status.HTTP_404_NOT_FOUND) 
    
    new_order = WorkOrder.objects.create(Submitter = user, description=description, Building_requested=unit)
    return_data['error_code'] = 0
    return HttpResponse(json.dumps(return_data),
                            content_type='application/json', status=status.HTTP_200_OK)

@api_view(http_method_names=['POST'])
def getOrder_API(request):
    print (request.data)

    return_data = {}

    getterEmail = request.data['email']

    try:
        user = User.objects.get(email=getterEmail)
    except:
        return_data['error_code'] = 1
        return HttpResponse(json.dumps(return_data),
                            content_type='application/json', status=status.HTTP_404_NOT_FOUND)
    
    all_order = []
    desired_format = '%Y-%m-%d'
    
    orders = WorkOrder.objects.filter(Submitter=user)
    for order in orders:
        if (order.RA_assigned is None):
            Ra = 'Not Assigned Yet'
        else:
            Ra = order.RA_assigned.name

        if (order.status is False):
            status_work='In Progress'
            End_time = 'In Progress'
        else:
            status_work='Done'
            End_time = order.End_time.strftime(desired_format)
        order_info = [order.Submit_time.strftime(desired_format), End_time, order.description, Ra, status_work]
        all_order.append(order_info)

    return_data['all_orders'] = all_order

    return_data['error_code'] = 0
    return HttpResponse(json.dumps(return_data),
                            content_type='application/json', status=status.HTTP_200_OK)


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

def sendWorkOrderPanel(request):
    template = loader.get_template('postOrder.html')
    return HttpResponse(template.render({}, request))

def getOrder(request):
    template = loader.get_template('DisplayOrders.html')
    return HttpResponse(template.render({}, request))

def logout(request):
    template = loader.get_template('logout.html')
    return HttpResponse(template.render({}, request))

