from django.urls import path
from .views import *

urlpatterns = [
    path('Users/', AllUserList.as_view()),
    path('homepage/', index, name="index"),
    path('signup/', signup, name="addUserCol"),
    path('SignupAPI/', SignupAPI, name="signupAPI"),
    path('deleteUserByID/<int:uid>', DeleteUserByID.as_view()),
]
