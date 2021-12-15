from django.urls import path
from .views import *

urlpatterns = [
    path('Users/', AllUserList.as_view()),
    path('login/', index, name="index"),
    path('signup/', signup, name="addUserCol"),
    path('SignupAPI/', SignupAPI.as_view()),
    path('LoginAPI/', UserLogIn, name="UserLogIn"),
    path('deleteUserByID/<int:uid>', DeleteUserByID.as_view()),
    path('homepage/', homePage, name="Homepage"),
    path('getNameViaEmail/', getNameViaEmail, name="getNameViaEmail"),
    path('testing/', test, name="test"),
    path('leasing/', leasing, name="leasing"),
    path('NewLeaseAPI/', NewLeaseAPI, name="NewLeaseAPI"),
    path('viewlease/', viewlease, name="viewlease"),
    path('messages/', messages, name="messages"),
    path('MessageAPI/', MessageAPI, name="MessageAPI"),
    path('viewInbox/', viewInbox, name="viewInbox"),
    path('viewOutbox/', viewOutbox, name="viewOutbox"),
]
