import sys

from django.db.models.query import QuerySet
from django.shortcuts import render, HttpResponse
from .serializer import UserSerializer
from django.http import JsonResponse
from .models import User
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import APIView
from django.template import loader

# Create your views here.
class AllUserList(APIView):
    def get(self, request):
        users = User.objects.all()
        Serializer = UserSerializer(users, many=True)
        return Response(Serializer.data)
    
    def post(self, request):
        print(request.data)
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED) # HTTP 201: CREATED
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) # HTTP 400: BAD REQUEST
    
    
def index(request):
    template = loader.get_template('index.html')
    return HttpResponse(template.render({}, request))

def signup(request):
    template = loader.get_template('Register.html')
    return HttpResponse(template.render({}, request))