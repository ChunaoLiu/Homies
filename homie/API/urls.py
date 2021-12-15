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
    path('getNumResident/', getTotalNumPeople, name="getTotalNumPeople"),
    path('postMsgAPI/', postMessage, name="postMessage"),
    path('homepage/SendMsgPanel/', sendMsgPanel, name="sendMsgPanel"),
    path('homepage/getMsgAPI/', getMessage, name="getMessage"),
    path('cheat/SetUnit_API/', set_Unit, name="set_unit"),
    path('AddWorkOrder_API/', order_add, name="workorder_add"),
    path('homepage/addWorkOrder/', sendWorkOrderPanel, name="sendWorkOrderPanel"),
    path('getOrder_API/', getOrder_API, name="getOrder"),
    path('homepage/getOrder/', getOrder, name="WorkOrder"),
]
